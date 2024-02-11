command = '/var/www/gameapi_01/APIForGame/env/bin/gunicorn'
python_path = '/var/www/gameapi_01/APIForGame/mainapp'
bind = '127.0.0.1:8001'
workers = 5
user = 'www'
raw_env = 'DJANGO_SETTINGS_MODULE=mainapp.settings'
