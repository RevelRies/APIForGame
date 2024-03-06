from .views import (UserDataView,
                    SaveUserDataView,
                    UserLeaderboardAllSeasonPosition,
                    UserLeaderboardCurrentSeasonPosition,
                    SeasonTopLeaderboard,
                    SeasonList,
                    PurchaseBooster,
                    PurchaseCharacter,
                    PurchaseQuiz,
                    SelectCharacter)

from django.urls import path


urlpatterns = [
    # path('', PurchaseBooster.as_view(), name='purchase_booster'),
    path('purchase/booster', PurchaseBooster.as_view(), name='purchase_booster'),
    path('purchase/character', PurchaseCharacter.as_view(), name='purchase_character'),
    path('purchase/quiz', PurchaseQuiz.as_view(), name='purchase_quiz'),
    path('save_user_data/', SaveUserDataView.as_view(), name='save_user_data'),
    path('season_top_leaderboard/', SeasonTopLeaderboard.as_view(), name='season_leaderboard'),
    path('season_list/', SeasonList.as_view(), name='season_list'),
    path('select_character/', SelectCharacter.as_view(), name='select_character'),
    path('user_data/', UserDataView.as_view(), name='user_data'),
    path('user_leaderboard_all_season/', UserLeaderboardAllSeasonPosition.as_view(), name='user_leaderboard_all_season'),
    path('user_leaderboard_current_season/', UserLeaderboardCurrentSeasonPosition.as_view(), name='user_leaderboard_current_season'),
]

app_name = 'game'
