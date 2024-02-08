#!/bin/bash
source /var/www/gameapi_01/env/bin/activate
exec gunicorn -c "/var/www/gameapi_01/APIForGame/mainapp/gunicorn_config.py" mainapp.wsgi
