# Generated by Django 4.2.9 on 2024-03-22 09:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_rank_image_datetime_alter_season_finish_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rank',
        ),
        migrations.AddField(
            model_name='userseasonscore',
            name='prize_received',
            field=models.BooleanField(default=False, verbose_name='приз получен'),
        ),
        migrations.AddField(
            model_name='userseasonscore',
            name='rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.rank', verbose_name='ранг'),
        ),
        migrations.AlterField(
            model_name='rank',
            name='image_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 9, 57, 0, 201520, tzinfo=datetime.timezone.utc), verbose_name='когда загружена картинка'),
        ),
        migrations.AlterField(
            model_name='season',
            name='finish_date',
            field=models.DateField(default=datetime.datetime(2024, 5, 21, 9, 57, 0, 219906, tzinfo=datetime.timezone.utc), verbose_name='дата окончания сезона'),
        ),
        migrations.AlterField(
            model_name='season',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 22, 9, 57, 0, 216824, tzinfo=datetime.timezone.utc), verbose_name='дата начала сезона'),
        ),
    ]
