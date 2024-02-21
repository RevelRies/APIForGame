from .views import (UserDataView,
                    SaveUserDataView,
                    UserLeaderboardPosition,
                    SeasonLeaderboard,
                    SeasonList)

from django.urls import path


urlpatterns = [
    path('user_data/', UserDataView.as_view(), name='user_data'),
    path('save_user_data/', SaveUserDataView.as_view(), name='save_user_data'),
    path('user_leaderboard/', UserLeaderboardPosition.as_view(), name='user_leaderboard'),
    path('season_leaderboard/', SeasonLeaderboard.as_view(), name='season_leaderboard'),
    path('season_list/', SeasonList.as_view(), name='season_list'),
]

app_name = 'game'