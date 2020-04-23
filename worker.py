import requests
import json
from TicketsFinder.aviasales import Aviasales
from TicketsFinder.tutu import Tutu
from TicketsFinder.tickets_finder import prepare_db_session, get_tickets_for_all_dections, get_return_tickets_for_all_directions
from datetime import datetime, timedelta
from dataclasses import asdict
from decimal import Decimal
from time import sleep


def find_trips(params):
    json_params = json.loads(params)

    origin_city = json_params['departure_city']
    depart_date = datetime.strptime('2020-05-02', '%Y-%m-%d')
    return_date = datetime.strptime('2020-05-03', '%Y-%m-%d')

    session = prepare_db_session()

    providers_list = []

    aviasales_provider = Aviasales(db_session=session)
    providers_list.append(aviasales_provider)

    tutu_provider = Tutu(db_session=session)
    providers_list.append(tutu_provider)

    print('One way tickets')
    search_result = get_tickets_for_all_dections(origin_city, depart_date, providers_list)

    print('Return tickets')
    search_result += get_return_tickets_for_all_directions(origin_city, depart_date, return_date, providers_list)

    dict_list = []
    for item in search_result:
        dict_list.append(asdict(item))

    price = lambda d: d['price'].compare(Decimal(json_params['max_price'])) == -1
    #airline = lambda d: d['airline'] == '7R'

    time_conditions = []
    for time_condition in json_params['time_for_travel']:
        if time_condition == 'far':
            time_conditions.append(timedelta(hours=9))
        elif time_condition == 'fair':
            time_conditions.append(timedelta(hours=6))
        elif time_condition == 'near':
            time_conditions.append(timedelta(hours=3))

    def time_for_travel(ticket):
        travel_time = ticket.get('travel_time')
        if travel_time is None:
            return True  # по-хорошему, нужно вернуть False
        travel_time = timedelta(seconds=travel_time)
        for time_condition in time_conditions:
            if travel_time < time_condition:
                return True
        return False

    filters = []
    filters.append(price)
    filters.append(time_for_travel)

    for current_filter in filters:
        dict_list = list(filter(current_filter, dict_list))

    result = {}
    result['search_result'] = dict_list
    if len(dict_list) > 0:
        result['status'] = 'OK'
    else:
        result['status'] = 'Failed'

    return result


def get_task():
    response = requests.get('http://127.0.0.1:8000/get_task/')
    if response.headers['Content-Type'] == 'application/json':
        print(response.json())
        return response.json()
    else:
        return {}


def process_task(task_data):
    result = find_trips(data['task_params'])
    task_data['status'] = result['status']
    task_data['task_result'] = json.dumps(result['search_result'], default=myconverter)
    return task_data


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
    if isinstance(o, Decimal):
        return o.__str__()


def commit_task(task_data):
    response = requests.post('http://127.0.0.1:8000/commit_task/', data=task_data)
    print(response)


if __name__ == '__main__':
    while True:
        sleep(60)
        data = get_task()
        if data.get('task_id') is None:
            print('no available tasks')
            continue
        else:
            print('task accepted')
            print(data)
        data = process_task(data)
        print(data)
        commit_task(data)
        print('processing finished')
