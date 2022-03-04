#!/bin/sh
export FLASK_ENV=development
export FLASK_APP=./app/index.py
source $(pipenv --venv)/bin/activate
flask run 