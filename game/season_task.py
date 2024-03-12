from datetime import timedelta

from models import Season

from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = ('Каждый день проверяет сколько осталось до конца текущего сезона'
            'Если осталась 1 минута, то функция создает новый сезон и делает его активным'
            'Проверка происходит в 23:58 по системному времени')

    def handle(self, *args, **options):
        # Проверяем равен ли день конца сезона сегодняшнему дню
        season = Season.objects.get(is_active=True)
        current_day = timezone.now().day
        # Если конец сезона сегодня, то создаем новый и делаем его активным
        if season.finish_date.day == current_day:
            number = season.number
            name = f"Season_{number}"
            # берем текущее время (23:58), прибавляем к нему час, заменяем часы и минуты на нули
            start_date = (timezone.now() + timedelta(hours=1)).replace(hour=0, minute=0, second=0)
            # продолжительность предыдущего сезона в днях
            length_prev_season = (season.finish_date - season.start_date).days
            # прибавляем к текущему времени продолжительность предыдущего сезона
            finish_date = ((timezone.localtime(timezone.now()) + timedelta(days=length_prev_season))
                           .replace(hour=23, minute=58, second=0))

            # создаем новый сезон
            Season.objects.create(name=name, number=number, start_date=start_date, finish_date=finish_date,
                                  is_active=True)

