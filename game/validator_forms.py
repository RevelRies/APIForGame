from .models import Season, Rank

from datetime import timedelta

from django import forms
from django.utils import timezone


class SeasonValidationForm(forms.ModelForm):
    def clean(self):
        # получаем значения из полей модели
        data = self.data
        ranks_qs = Rank.objects.all()
        # составляем список id существующих рангов
        ranks_id_list = [rank.pk for rank in ranks_qs]
        ranks_id_checklist = list()

        # записываем id рангов для которых пользователь создал призы
        for indx in range(len(ranks_qs)):
            try:
                rank_id = data[f'prize_set-{indx}-rank']
                ranks_id_checklist.append(int(rank_id))
            except:
                raise forms.ValidationError('В сезоне для каждого ранга должны быть законфигурированны призы')

        # проверяется чтобы для каждого ранга в сезоне был создан приз
        if sorted(ranks_id_list) != sorted(ranks_id_checklist):
            raise forms.ValidationError('В сезоне для каждого ранга должны быть законфигурированны призы')

        # проверяем чтобы для каждого игрока в топ 3 был добавлен отдельный приз
        prizetop3_top_number_list = list()
        for indx in range(3):
            try:
                top_number = data[f"prizetop3_set-{indx}-top_number"]
                prizetop3_top_number_list.append(int(top_number))
            except:
                raise forms.ValidationError('В сезоне для каждого игрока из топ 3 должны быть законфигурированны призы')

        if sorted(prizetop3_top_number_list) != [1, 2, 3]:
            raise forms.ValidationError('В сезоне для каждого игрока из топ 3 должны быть законфигурированны призы')

        # # если это новый сезон
        # if not Season.objects.filter(number=data['number']).exists():
        #     # создание самого первого сезона
        #     if not Season.objects.all().exists():
        #         # проверяем чтобы дата начала была не позже сегодня
        #         if data['start_date'] > (timezone.localtime(timezone.now())).date():
        #             raise forms.ValidationError('Дата окончания сезона не может быть раньше даты начала')
        #     # создание не первого сезона
        #     else:
        #         prev_season = Season.objects.all().last()
        #         # проверка чтобы дата начала у нового сезона была после даты конца пред сезона
        #         if data['start_date'] != prev_season.finish_date + timedelta(days=1):
        #             raise forms.ValidationError('Дата начала сезона должна быть на следующий день окончания предыдущего сезона')
        #     # проверка чтобы дата конца сезона была после даты его начала
        #     if data['finish_date'] <= data['start_date']:
        #         raise forms.ValidationError('Дата окончания сезона должна быть после даты его начала')
        #
        # # если это редактирование существующего сезона
        # else:
        #     last_season_number = Season.objects.all().last().number
        #
        #     # проверка чтобы дата конца сезона была после даты его начала
        #     if data['finish_date'] <= data['start_date']:
        #         raise forms.ValidationError('Дата окончания сезона должна быть после даты его начала')
        #
        #     # если это первый сезон - проверяем чтобы дата начала была не позже сегодня
        #     if data['number'] == 1:
        #         if data['start_date'] > (timezone.localtime(timezone.now())).date():
        #             raise forms.ValidationError('Дата окончания сезона не может быть раньше даты начала')
        #
        #     # если это первый и не последний сезон - проверяем чтобы дата конца была до начала 2 сезона
        #     if data['number'] == 1 and last_season_number != 1:
        #         raise forms.ValidationError('Дата окончания сезона не может быть раньше даты начала следующего сезона')
        #
        #     # если это сезон, который находится между двумя - проверяем чтобы дата начала не совпадала с датой конца
        #     # предыдущего сезона и дата конца не совпадала с датой начала следующего сезона
        #     elif last_season_number != instance.number:
        #         if data['start_date'] <= Season.objects.get(number=last_season_number - 1).finish_date:
        #             raise forms.ValidationError('Дата начала сезона должна быть на следующий день окончания предыдущего сезона')
        #         if data['finish_date'] >= Season.objects.get(number=last_season_number + 1).start_date:
        #             raise forms.ValidationError('Дата окончания сезона должна быть за день до начала следующего сезона')
        #
        #     # если это последний сезон и он не первый - проверяем чтобы дата начала не совпадала с датой конца предыдущего сезона
        #     elif last_season_number == data['number'] and last_season_number != 1:
        #         if data['start_date'] <= Season.objects.get(number=last_season_number - 1).finish_date:
        #             raise forms.ValidationError('Дата начала сезона должна быть на следующий день окончания предыдущего сезона')