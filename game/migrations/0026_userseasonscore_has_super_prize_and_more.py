# Generated by Django 4.2.9 on 2024-03-23 08:22

import datetime
from django.db import migrations, models
import django_jsonform.models.fields
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_remove_user_rank_userseasonscore_prize_received_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userseasonscore',
            name='has_super_prize',
            field=models.BooleanField(default=False, verbose_name='супер приз имеется'),
        ),
        migrations.AddField(
            model_name='userseasonscore',
            name='super_prize_received',
            field=models.BooleanField(default=False, verbose_name='супер приз получен'),
        ),
        migrations.AlterField(
            model_name='prize',
            name='boosters',
            field=django_jsonform.models.fields.JSONField(blank=True, default={'Invincibility': 0, 'Magnet': 0, 'Speed': 0}, validators=[game.models.User.validate_boosters], verbose_name='бустеры'),
        ),
        migrations.AlterField(
            model_name='prizetop3',
            name='boosters',
            field=django_jsonform.models.fields.JSONField(blank=True, default={'Invincibility': 0, 'Magnet': 0, 'Speed': 0}, validators=[game.models.User.validate_boosters], verbose_name='бустеры'),
        ),
        migrations.AlterField(
            model_name='rank',
            name='image_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 23, 8, 22, 9, 825763, tzinfo=datetime.timezone.utc), verbose_name='когда загружена картинка'),
        ),
        migrations.AlterField(
            model_name='season',
            name='finish_date',
            field=models.DateField(default=datetime.datetime(2024, 5, 22, 8, 22, 9, 833770, tzinfo=datetime.timezone.utc), verbose_name='дата окончания сезона'),
        ),
        migrations.AlterField(
            model_name='season',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 23, 8, 22, 9, 832769, tzinfo=datetime.timezone.utc), verbose_name='дата начала сезона'),
        ),
    ]
