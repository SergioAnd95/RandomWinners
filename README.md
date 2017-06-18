# RandomWinners
Test №2 for Evo company, and build on Python3.6/Django1.11

## Running web-app on testing web-server you can see here:
https://stark-ridge-81752.herokuapp.com


## Before start:
Creaete virtualenvironmet and activate(not required):

```virtualenv venv```

`source env/bin/activate`

## Clone repository:
`git clone https://github.com/SergioAnd95/UpdateConfig.git`

## Go to derictory:
`cd RandomWinners`

## Now you must install all requirements for project:
`pip install -r requirements.txt`

## Make migrations to your DB:
`./manage.py migrate`

## Now you ready to run project:
`./manage.py runserver`

## Addional

### Tests
if you want to run tests, you can do this with this command:

`./manage.py test`

### Create superuser
`./manage.py createsuperuser`
