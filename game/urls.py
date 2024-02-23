from .views import (UserDataView,
                    SaveUserDataView,
                    UserLeaderboardAllSeasonPosition,
                    UserLeaderboardCurrentSeasonPosition,
                    SeasonTopLeaderboard,
                    SeasonList)

from django.urls import path


urlpatterns = [
    path('user_data/', UserDataView.as_view(), name='user_data'),
    path('save_user_data/', SaveUserDataView.as_view(), name='save_user_data'),
    path('user_leaderboard_all_season/', UserLeaderboardAllSeasonPosition.as_view(), name='user_leaderboard_all_season'),
    path('user_leaderboard_current_season/', UserLeaderboardCurrentSeasonPosition.as_view(), name='user_leaderboard_current_season'),
    path('season_top_leaderboard/', SeasonTopLeaderboard.as_view(), name='season_leaderboard'),
    path('season_list/', SeasonList.as_view(), name='season_list'),
]

app_name = 'game'
