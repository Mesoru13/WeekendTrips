# WeekendTrips
Project's goal is to deliver for users an advice of trip on selected weekend.

## Prerequisites
Firstly install python 3.7 or newer

## Installing
1. clone this repo
2. init submodules
```
git submodule update --init
```
3. prepare virtual environment
```
python3 -m venv env
source ./env/bin/activate
```
4. install all reqs
```
pip install -r ./requirements.txt
pip install -r ./TicketsFinder/requirements.txt
```
5. prepare databases from TicketsFinder
```
cd TicketsFinder
alembic upgrade head
cd ..
```
## Launching
1. run server
```
python manage.py runserver
```
2. in web browser configure params and press "Find my trip!" button
3. open second terminal window with activated venv
4. launch worker script. [optional] use TRAVEL_PAYOUTS_TOKEN env var to provide aviasales api token
```
TRAVEL_PAYOUTS_TOKEN='<token>' python ./worker.py
```
5. Profit!
