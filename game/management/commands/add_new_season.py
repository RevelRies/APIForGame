from datetime import timedelta

from game.models import Season, UserSeasonScore, User, Rank, Prize, PrizeTop3, SuperPrize

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
            current_season = Season.objects.get(is_active=True)
            if current_season == Season.objects.all().last():
                number = prev_season.number + 1
                name = f"season_{number}"
                # берем текущее время (23:59), прибавляем к нему час, заменяем часы и минуты на нули
                start_date = (timezone.localtime(timezone.now()) + timedelta(days=1)).date()
                # продолжительность предыдущего сезона в днях
                length_prev_season = (prev_season.finish_date - prev_season.start_date).days + 1
                # прибавляем к текущему времени продолжительность предыдущего сезона
                finish_date = ((timezone.localtime(timezone.now()) + timedelta(days=length_prev_season))).date()
    
                # создаем новый сезон и призы для нового сезона (копируются с предыдущего)
                new_season = Season.objects.create(name=name, number=number, start_date=start_date, finish_date=finish_date,
                                      is_active=True)

                # призы по рангам
                for rank in Rank.objects.all():
                    prev_prize = Prize.objects.get(rank=rank, season=current_season)
                    Prize.objects.create(rank=rank,
                                         season=new_season,
                                         coins=prev_prize.coins,
                                         characters=prev_prize.characters,
                                         boosters=prev_prize.boosters)
                # призы для топ 3
                for top_number in range(1, 4):
                    prev_prize_top_3 = PrizeTop3.objects.get(top_number=top_number, season=current_season)
                    PrizeTop3.objects.create(top_number=top_number,
                                             season=new_season,
                                             coins=prev_prize_top_3.coins,
                                             characters=prev_prize_top_3.characters,
                                             boosters=prev_prize_top_3.boosters)
                # супер приз
                prev_super_prize = SuperPrize.objects.get(season=current_season)
                SuperPrize.objects.create(season=new_season,
                                          name=prev_super_prize.name,
                                          image_preview=prev_super_prize.image_preview,
                                          image_gift=prev_super_prize.image_gift,
                                          description=prev_super_prize.description,
                                          burns_down_date=prev_super_prize.burns_down_date)

            # если новый сезон уже законфигурирован, то просто делаем его активным
            else:
                next_season = Season.objects.get(number=prev_season.number + 1)
                next_season.is_active = True
                next_season.save()

            # берем первого пользователя в конце сезона и помечаем что он имеет супер приз
            top1_user_season_score = (UserSeasonScore.objects.
                                      filter(season=current_season).
                                      order_by('-season_high_score').
                                      first())
            top1_user_season_score.has_super_prize = True
            top1_user_season_score.save()

            prev_season.is_active = False
            prev_season.save()

