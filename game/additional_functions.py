from .models import User, Season, UserSeasonScore, Booster, Character, Rank

from django.core.exceptions import ValidationError

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

    def get_quantity_by_percentage(quantity_users, rank):
        # сумма процентов предыдущих рангов
        if rank.number != 1:
            minus_percent = Rank.objects.get(number=rank.number - 1).min_percent_users
        else:
            minus_percent = 0

        # минимум людей, который должен быть в этом ранге (по процентам)
        percent = rank.min_percent_users - minus_percent
        return round((quantity_users / 100) * percent)


    all_user_season_scores = (UserSeasonScore.objects.
                              filter(season=Season.objects.get(is_active=True)).
                              order_by("-season_high_score"))
    all_ranks = Rank.objects.all()

    quantity_users = len(all_user_season_scores)

    # если хоть в одном ранге недобор по количеству пользователей в %, то во всех рангах испольхуем ограничение по кол-ву
    is_percent_limit = True
    # в списке каждое число означает сколько пользователей (по процентам) должно быть в ранге. индекс 0 == ранк 1 и т.д.
    quantity_users_in_ranks = []
    for rank in all_ranks:
        num = get_quantity_by_percentage(quantity_users, rank)
        if num < rank.min_int_users:
            is_percent_limit = False
            break
        quantity_users_in_ranks.append(num)

    # если рапределяем не по процентам, то написываем в список сколько пользователей должн быть по int ограничению
    if not is_percent_limit:
        quantity_users_in_ranks.clear()
        for rank in all_ranks:
            quantity_users_in_ranks.append(rank.min_int_users)

    # распределение пользователей по рангам
    uss_iterator = iter(all_user_season_scores)

    # берем каждый ранг
    for rank_number in range(1, len(quantity_users_in_ranks) + 1):
        rank = Rank.objects.get(number=rank_number)

        # берем количество пользователей из списка и засовываем в текущий ранг
        for _ in range(quantity_users_in_ranks[rank_number - 1]):
            try:
                uss = next(uss_iterator)
                uss.user.rank = rank
                uss.user.save()
            except:
                pass

    # оставшихся пользователей оставляем бех ранга
    while 1:
        try:
            uss = next(uss_iterator)
            uss.user.rank = None
            print(f"{uss.user.username} - {uss.user.rank}")
            uss.user.save()
        except:
            break







