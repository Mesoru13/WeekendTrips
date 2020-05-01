from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from .forms import InputDataForm
from .models import TaskRequest
from WeekendTrips.settings import STATIC_ROOT
import json
import uuid
import io

cities = []


def sort_requests_by_datetime(requests):
    return requests


def extract_data_from_post(post_request):
    data = post_request.dict()
    data['time_for_travel'] = dict(post_request.lists()).get('time_for_travel')
    return data


def get_cities_by_filter(city_filter):
    if len(cities) == 0:
        path = STATIC_ROOT + '/cities.txt'
        with io.open(path, encoding='utf-8') as file:
            for line in file:
                cities.append(line)
    data = []
    for city in cities:
        if city_filter in city:
            data.append(city)
    return data


def home(request):
    yandex_api_key = '9a01f7c3-d337-4582-a99b-a765051710ed'
    are_previous_results_available = False
    if request.method == 'GET':
        form = InputDataForm()
        task_id = request.GET.get('task_id')
        if task_id is not None:
            task_request = TaskRequest.objects.get(task_id=task_id)
            task_params = json.loads(task_request.json_task_params)
            form = InputDataForm(task_params)
            if task_request.request_status == 1003:
                are_previous_results_available = True
        response = render(request, 'home.html',
                          {'form': form,
                           'task_id': task_id,
                           'yandex_api_key': yandex_api_key,
                           'are_previous_results_available': are_previous_results_available,
                           'form_error_message': ''})
        return response
    elif request.method == 'POST':

        input_data = InputDataForm(data=extract_data_from_post(request.POST))
        task_params = json.dumps(input_data.data,
                                 ensure_ascii=False)

        task_id = request.GET.get('task_id')
        task_request = None
        if task_id is None:
            task_id = uuid.uuid4().hex
            task_request = TaskRequest(task_id=task_id,
                                       json_task_params=task_params)
        else:
            task_request = TaskRequest.objects.get(task_id=task_id)
            task_request.json_task_params = task_params

        response = None
        if input_data.is_valid():
            task_request.request_status = 1001
            response = HttpResponseRedirect('/results/?task_id={}'.format(task_id))
        else:
            response = render(request, 'home.html',
                              {'form': input_data,
                               'yandex_api_key': yandex_api_key,
                               'are_previous_results_available': are_previous_results_available})
        task_request.save()
        return response


def results(request):
    if request.method == 'GET':
        if request.GET.get('task_id') is None:
            return HttpResponseRedirect(reverse('home'))
        else:
            task_id = request.GET.get('task_id')
            task_request = TaskRequest.objects.get(task_id=task_id)
            json_task_result = json.loads(task_request.json_task_result)
            if task_request.request_status == 1001 \
                    or task_request.request_status == 1002 \
                    or task_request.request_status == 1004:
                return render(request, 'results.html', {'task_id': task_id,
                                                        'status': task_request.request_status})
            elif task_request.request_status == 1003:
                json_result = json.loads(task_request.json_task_result)
            return render(request, 'results.html', {'task_id': task_id,
                                                    'status': task_request.request_status,
                                                    'json_result': json_task_result})


def get_cities(request):
    if request.method == 'GET':
        response_data = []
        if not request.GET.get('q') is None:
            response_data = get_cities_by_filter(request.GET.get('q'))
        response = JsonResponse(response_data, safe=False)
        response.status_code = 200
        return response


@csrf_exempt
def get_task(request):
    if request.method == 'GET':
        task_requests = TaskRequest.objects.filter(request_status=1001)
        task_requests = sort_requests_by_datetime(task_requests)

        response = HttpResponse()
        response.status_code = 200
        if len(task_requests) > 0:
            response_data = {
                'task_id': task_requests[0].task_id,
                'task_params': task_requests[0].json_task_params
            }
            response = JsonResponse(response_data)
            task_request = TaskRequest.objects.get(task_id=task_requests[0].task_id)
            task_request.request_status = 1002
            task_request.save()

        return response
    else:
        return HttpResponseBadRequest('get_task works only in GET')


@csrf_exempt
def commit_task(request):
    if request.method == 'POST':
        if request.POST.get('task_id') is None \
                or request.POST.get('status') is None:
            return HttpResponseBadRequest('task_id or status or both were not provided')
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')

        task_request = TaskRequest.objects.get(task_id=task_id)
        if status == 'OK':
            task_request.request_status = 1003
            if request.POST.get('task_result') is None:
                return HttpResponseBadRequest('task_result was not provided with successful search')
            else:
                task_request.json_task_result = request.POST.get('task_result')
        else:
            task_request.request_status = 1004
        task_request.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest('commit_task works only in POST')


def get_task_result(request):
    if request.method == 'GET':
        task_id = request.GET.get('task_id')
        task_results = {
            'task_result': TaskRequest.objects.get(task_id=task_id).json_task_result,
            'request_status': TaskRequest.objects.get(task_id=task_id).request_status
        }
        response = JsonResponse(task_results, safe=False)
        response.status_code = 200
        return response
    else:
        return HttpResponseBadRequest('get_task works only in GET')