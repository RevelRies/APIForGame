from .models import User, Season, UserSeasonScore, Booster, Character, Rank

def get_user_position(user: User, season: Season):
    '''
    Получаем позицию пользователя в сезоне в соответствии с его season_high_score
    '''
    current_user_season_score = UserSeasonScore.objects.get(season=season, user=user)

    # получаем словарь из объектов QuerySet
    # фильтрация происходит в таком порядке
    # 1 - QS текущего сезона
    # 2 - фильтруем по убыванию season_high_score
    # 3 - QS у которых season_high_score больше либо равен season_high_score данного пользователя
    # 4 - фильтруем по username пользователей
    user_season_score_qs = (UserSeasonScore.objects.
                            filter(season=season).
                            order_by("-season_high_score"))

    return list(user_season_score_qs.values_list('id', flat=True)).index(current_user_season_score.id) + 1


def editing_ranks():
    '''
    Функция вызывается после каждого забега
    При вызове, пользователи редактируются ранги игры в части напосления пользователями
    '''

    def get_quantity_by_percentage(percent, num):
        return round((num / 100) * percent)

    all_user_season_scores = (UserSeasonScore.objects.
                              filter(season=Season.objects.get(is_active=True)).
                              order_by("-season_high_score"))


    quantity_users = len(all_user_season_scores)


    # вычисляем количество пользователей для каждого ранга
    # 1 Ранг
    rank_1 = Rank.objects.get(number=1)
    users_quantity_rank_1 = max(rank_1.min_int_users,
                                get_quantity_by_percentage(rank_1.min_percent_users, quantity_users))
    # 2 Ранг
    rank_2 = Rank.objects.get(number=2)
    users_quantity_rank_2 = max(rank_2.min_int_users,
                                get_quantity_by_percentage(rank_2.min_percent_users, quantity_users))
    # 3 Ранг
    rank_3 = Rank.objects.get(number=3)
    users_quantity_rank_3 = max(rank_3.min_int_users,
                                get_quantity_by_percentage(rank_3.min_percent_users, quantity_users))

    # делаем итератор из user_season_scores
    uss_iterator = iter(all_user_season_scores)

    # засовываем нужное количество пользователей в ранг 1
    for _ in range(users_quantity_rank_1):
        try:
            user_season_score = next(uss_iterator)
            print(user_season_score.user.username)
            user_season_score.user.rank = rank_1
            user_season_score.user.save()
        except:
            break

    # засовываем нужное количество пользователей в ранг 2
    for _ in range(users_quantity_rank_2):
        try:
            user_season_score = next(uss_iterator)
            user_season_score.user.rank = rank_2
            user_season_score.user.save()
        except:
            break

    # засовываем нужное количество пользователей в ранг 3
    for _ in range(users_quantity_rank_3):
        try:
            user_season_score = next(uss_iterator)
            user_season_score.user.rank = rank_3
            user_season_score.user.save()
        except:
            break




