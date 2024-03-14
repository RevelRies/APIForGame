from datetime import timedelta

from game.models import Season

from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = ('Каждый день проверяет сколько осталось до конца текущего сезона'
            'Если осталась 1 минута, то функция создает новый сезон и делает его активным'
            'Если новый сезон создан, то делает его активным'
            'Проверка происходит в 23:59 по системному времени')

    def handle(self, *args, **options):
        print("Отрабатывает команда создания сезона")

        # Проверяем равен ли день конца сезона сегодняшнему дню
        prev_season = Season.objects.get(is_active=True)
        current_day = (timezone.localtime(timezone.now())).day
        # Если конец сезона сегодня, то проверяем законфигурирован ли следующий сезон
        if prev_season.finish_date.day == current_day:
            # Если следующий сезон не законфигурирован, то создаем новый и делаем его активным
            if Season.objects.get(is_active=True) == Season.objects.all().last():
                number = prev_season.number + 1
                name = f"season_{number}"
                # берем текущее время (23:59), прибавляем к нему час, заменяем часы и минуты на нули
                start_date = (timezone.localtime(timezone.now()) + timedelta(days=1)).date()
                # продолжительность предыдущего сезона в днях
                length_prev_season = (prev_season.finish_date - prev_season.start_date).days + 1
                # прибавляем к текущему времени продолжительность предыдущего сезона
                finish_date = ((timezone.localtime(timezone.now()) + timedelta(days=length_prev_season))).date()
    
                # создаем новый сезон
                Season.objects.create(name=name, number=number, start_date=start_date, finish_date=finish_date,
                                      is_active=True)
            # если новый сезон уже законфигурирован, то просто делаем его активным
            else:
                next_season = Season.objects.get(number=prev_season.number + 1)
                next_season.is_active = True
                next_season.save()

            prev_season.is_active = False
            prev_season.save()

