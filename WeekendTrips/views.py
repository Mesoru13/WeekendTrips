from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import InputDataForm
from .models import Result
import json
from time import sleep


def find_trips(data):
    a = [
            {'type': 'flight', 'origin': 'Москва', 'destination': 'Сочи', 'number': 1130, 'airline': 'SU', 'price': 16487, 'departure_at': '2020-03-21T22:55:00Z', 'return_at': '2020-03-22T10:45:00Z'},
            {'type': 'train', 'seat': 'Нижние', 'price': '13735', 'number': '104В', 'time': '1д. 1ч.', 'origin': 'Москва', 'destination': 'Сочи'}
        ]
    return a


def home(request):
    if request.method == 'GET':
        are_previous_results_available = False
        is_session_id_available = False
        current_session_id = ''
        if request.COOKIES.get('session_id') is not None:
            cookies_session_id = request.COOKIES.get('session_id')
            model = Result.objects.get(session_id=cookies_session_id)
            if model is not None:
                is_session_id_available = True
                current_session_id = cookies_session_id
                if model.json_result != '':
                    are_previous_results_available = True

        if not is_session_id_available:
            current_session_id = str(Result.objects.count() + 1)
            model = Result(session_id=current_session_id, json_result="")
            model.save()

        form = InputDataForm()
        response = render(request, 'home.html',
                          {'form': form, 'are_previous_results_available': are_previous_results_available})
        if not is_session_id_available:
            response.set_cookie('session_id', current_session_id)
        return response
    elif request.method == 'POST':
        current_session_id = request.COOKIES.get('session_id')
        model = Result.objects.get(session_id=current_session_id)
        form = InputDataForm(request.POST)
        json_result = find_trips(form)
        sleep(120)
        model.json_result = json.dumps(json_result)
        model.save()
        return HttpResponseRedirect(reverse('results'))


def results(request):
    if request.method == 'GET':
        if request.COOKIES.get('session_id') is None:
            return HttpResponseRedirect(reverse('home'))
        else:
            current_session_id = request.COOKIES.get('session_id')
            model = Result.objects.get(session_id=current_session_id)
            json_result = json.loads(model.json_result)
            return render(request, 'results.html', {'json_result': json_result})