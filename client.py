import requests
from time import sleep
import json

def find_trips(params):
    results = {
        'status': 'OK',
        'search_result': [
            {'type': 'flight', 'origin': 'Москва', 'destination': 'Сочи', 'number': 1130, 'airline': 'SU', 'price': 16487, 'departure_at': '2020-03-21T22:55:00Z', 'return_at': '2020-03-22T10:45:00Z'},
            {'type': 'train', 'seat': 'Нижние', 'price': '13735', 'number': '104В', 'time': '1д. 1ч.', 'origin': 'Москва', 'destination': 'Сочи'}
        ]
    }
    return results


def get_task():
    response = requests.get('http://127.0.0.1:8000/get_task/')
    task_id = response.headers.get('task_id')
    task_params = response.headers.get('task_params')
    task_data = {
        'task_id': task_id,
        'task_params': task_params
    }
    return task_data


def process_task(task_data):
    result = find_trips(data['task_params'])
    task_data['status'] = result['status']
    task_data['task_result'] = json.dumps(result['search_result'])
    return task_data


def commit_task(task_data):
    response = requests.post('http://127.0.0.1:8000/commit_task/', data=task_data)
    print(response)

if __name__ == '__main__':
    #while True:
    sleep(60)
    data = get_task()
    if data['task_id'] is None:
        exit(0)
    print(data)
    data = process_task(data)
    print(data)
    commit_task(data)
    print('commit')
