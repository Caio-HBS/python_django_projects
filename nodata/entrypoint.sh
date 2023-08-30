#!/bin/sh

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
export DJANGO_SUPERUSER_USERNAME=staff
export DJANGO_SUPERUSER_EMAIL=test@email.com
export DJANGO_SUPERUSER_PASSWORD=staffuserpassword
python3 manage.py createsuperuser --no-input

gunicorn nodata.wsgi:application --bind 0.0.0.0:8000