# Generated by Django 4.2.9 on 2024-01-26 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название сезона')),
                ('number', models.IntegerField(verbose_name='номер сезона')),
                ('start_date', models.DateTimeField(verbose_name='время начала сезона')),
                ('finish_date', models.DateTimeField(verbose_name='время окончания сезона')),
                ('prize', models.CharField(blank=True, max_length=250, verbose_name='приз сезона')),
            ],
        ),
        migrations.CreateModel(
            name='UserSeasonScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_high_score', models.IntegerField(default=0, verbose_name='максимальный результат пользователя в сезоне')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.season')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_time_score', models.IntegerField(default=0, verbose_name='количество очков за все время')),
                ('all_time_high_score', models.IntegerField(default=0, verbose_name='максимальный результат за все время')),
                ('coins', models.IntegerField(default=0, verbose_name='количество монет у пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
