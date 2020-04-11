import requests
import json
from TicketsFinder.aviasales import Aviasales
from TicketsFinder.tutu import Tutu
from TicketsFinder.tickets_finder import prepare_db_session, get_tickets
from datetime import datetime
from dataclasses import asdict
from decimal import Decimal


def find_trips(params):
    json_params = json.loads(params)

    origin_city = json_params['departure_city']
    destination_city = 'Сочи'
    depart_date = datetime.strptime('2020-04-21', '%Y-%m-%d')
    return_date = datetime.strptime('2020-04-22', '%Y-%m-%d')

    session = prepare_db_session()

    providers_list = []

    aviasales_provider = Aviasales(db_session=session)
    providers_list.append(aviasales_provider)

    tutu_provider = Tutu(db_session=session)
    providers_list.append(tutu_provider)

    print('One way tickets')
    search_result = get_tickets(origin_city, destination_city, depart_date, providers_list)

    dict_list = []
    for item in search_result:
        dict_list.append( asdict(item) )

    result = {}
    result['search_result'] = dict_list
    if len(dict_list) > 0:
        result['status'] = 'OK'
    else:
        result['status'] = 'Failed'

#    print('Return tickets')
#    print(get_return_tickets(origin_city, destination_city, depart_date, return_date, providers_list))
    return result


"""
def find_trips(params):
    results = {
        'status': 'OK',
        'search_result': [
            {'type': 'flight', 'origin': 'Москва', 'destination': 'Сочи', 'number': 1130, 'airline': 'SU', 'price': 16487, 'departure_at': '2020-03-21T22:55:00Z', 'return_at': '2020-03-22T10:45:00Z'},
            {'type': 'train', 'seat': 'Нижние', 'price': '13735', 'number': '104В', 'time': '1д. 1ч.', 'origin': 'Москва', 'destination': 'Сочи'}
        ]
    }
    return results
"""

def get_task():
    response = requests.get('http://127.0.0.1:8000/get_task/')
    print(response.json())
    return response.json()


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
    #while True:
    #sleep(60)
    data = get_task()
    if data['task_id'] is None:
        print('no available tasks')
        exit(0)
    else:
        print('task accepted')
        print(data)
    data = process_task(data)
    print(data)
    commit_task(data)
    print('processing finished')
