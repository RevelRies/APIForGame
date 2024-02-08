command = '/var/www/gameapi_01/env/bin/gunicorn'
python_path = '/var/www/gameapi_01/APIForGame/mainapp'
bind = '0.0.0.0:8001'
workers = 5
user = 'www'
raw_env = 'DJANGO_SETTINGS_MODULE=mainapp.settings'
