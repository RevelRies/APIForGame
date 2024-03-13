from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from pytz import timezone

def start():
    scheduler = BackgroundScheduler(timezone=timezone('Europe/Moscow'))
    scheduler.add_job(call_command, 'cron', hour=23, minute=59, args=['add_new_season'])
    scheduler.start()