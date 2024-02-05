from .views import (UserDataView,
                    SaveScoreView,
                    SaveCoinsView,
                    UserLeaderboardPosition,
                    SeasonLeaderboard)

from django.urls import path


urlpatterns = [
    path('user_data/', UserDataView.as_view(), name='user_data'),
    path('save_score/', SaveScoreView.as_view(), name='save_score'),
    path('save_coins/', SaveCoinsView.as_view(), name='save_coins'),
    path('user_leaderboard/', UserLeaderboardPosition.as_view(), name='user_leaderboard'),
    path('season_leaderboard/', SeasonLeaderboard.as_view(), name='season_leaderboard'),
]

app_name = 'game'