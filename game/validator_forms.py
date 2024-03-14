from .models import Season

from datetime import timedelta

from django import forms
from django.utils import timezone


class SeasonValidationForm(forms.ModelForm):
    def clean(self):
        data = self.cleaned_data
        print(data)

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