import requests
import json
from TicketsFinder.aviasales import Aviasales
from TicketsFinder.tutu import Tutu
from TicketsFinder.tickets_finder import prepare_db_session, get_tickets_for_all_directions, get_return_tickets_for_all_directions
from datetime import datetime, timedelta, time
from dataclasses import asdict
from decimal import Decimal
from time import sleep


def find_trips(params):
    json_params = json.loads(params)

    origin_city = json_params['departure_city']
    depart_date = datetime.strptime(json_params['start_date'], '%Y-%m-%d')
    return_date = datetime.strptime(json_params['end_date'], '%Y-%m-%d')
    session = prepare_db_session()

    providers_list = []

    aviasales_provider = Aviasales(db_session=session)
    providers_list.append(aviasales_provider)

    tutu_provider = Tutu(db_session=session)
    providers_list.append(tutu_provider)

    print('One way tickets')
    search_result = get_tickets_for_all_directions(origin_city, depart_date, providers_list)

    print('Return tickets')
    search_result += get_return_tickets_for_all_directions(origin_city, depart_date, return_date, providers_list)

#    list_of_tickets = convert_tickets_to_dicts(search_result)

    # фильтр по цене
    price = lambda d: d.price.compare(Decimal(json_params['max_price'])) == -1

    # фильтр по времени в пути
    time_conditions = []
    for time_condition in json_params['time_for_travel']:
        if time_condition == 'far':
            time_conditions.append(timedelta(hours=9))
        elif time_condition == 'fair':
            time_conditions.append(timedelta(hours=6))
        elif time_condition == 'near':
            time_conditions.append(timedelta(hours=3))

    def time_for_travel(ticket):
        if ticket.route_type == 'train:':
            travel_time = ticket.travel_time  # get('travel_time')
            travel_time = timedelta(seconds=travel_time)
            for time_condition in time_conditions:
                if travel_time < time_condition:
                    return True
            return False
        return True  # по-хорошему, нужно вернуть False

    # составляем список всех фильров
    filters = []
    filters.append(price)
    filters.append(time_for_travel)

    # фильтуем результат
    search_result = filter_tickets(search_result, filters)

    # сортируем по удобности
    search_result = sort_tickets(search_result)

    list_of_tickets = convert_tickets_to_dicts(search_result)

    result = generate_result(list_of_tickets)
    return result


# попробуем вывести наверх списка удобные билеты
def sort_tickets(tickets):
    for ticket in tickets:
        if ticket.arrival_time is not None:
            if time(hour=8) < ticket.arrival_time < time(hour=13):
                ticket.nice += 10
            elif time(hour=13) < ticket.arrival_time < time(hour=23, minute=59):
                ticket.nice -= 10
            elif time(hour=0) < ticket.arrival_time < time(hour=8):
                ticket.nice -= 10

            if ticket.arrival_date.weekday() != 5:
                ticket.nice -= 30

        if time(hour=0) < ticket.depart_time < time(hour=6):
            ticket.nice -= 10

    return sorted(tickets, key=lambda x: x.nice, reverse=True)


def convert_tickets_to_dicts(raw_tickets):
    list_of_tickets = []
    for item in raw_tickets:
        list_of_tickets.append(asdict(item))
    return list_of_tickets


def generate_result(list_of_tickets):
    result = {}
    result['search_result'] = list_of_tickets
    if len(list_of_tickets) > 0:
        result['status'] = 'OK'
    else:
        result['status'] = 'Failed'

    return result


def filter_tickets(list_of_tickets, filters):
    for current_filter in filters:
        list_of_tickets = list(filter(current_filter, list_of_tickets))
    return list_of_tickets


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
    task_data['task_result'] = json.dumps(result['search_result'], default=myconverter, ensure_ascii=False)
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
        data = get_task()
        if data.get('task_id') is None:
            print('no available tasks')
            sleep(60)
            continue
        else:
            print('task accepted')
            print(data)
        data = process_task(data)
        print(data)
        commit_task(data)
        print('processing finished')
