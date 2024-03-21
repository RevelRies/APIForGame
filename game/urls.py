from .views import (UserDataView,
                    SaveUserDataView,
                    UserLeaderboardAllSeasonPosition,
                    UserLeaderboardCurrentSeasonPosition,
                    SeasonTopLeaderboard,
                    SeasonList,
                    PurchaseBooster,
                    PurchaseCharacter,
                    PurchaseQuiz,
                    SelectCharacter,
                    BoostersList,
                    CharactersList,
                    EditBooster,
                    RanksList,
                    PrizeList,
                    PrizeTop3List,
                    SuperPrizeView)

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('boosters_list/', BoostersList.as_view(), name='boosters_list'),
    path('character_list/', CharactersList.as_view(), name='character_list'),
    path('edit_boosters/', EditBooster.as_view(), name='edit_boosters'),
    path('prizes/', PrizeList.as_view(), name='prizes'),
    path('prizes_top_3/', PrizeTop3List.as_view(), name='prizes_top_3'),
    path('purchase/booster/', PurchaseBooster.as_view(), name='purchase_booster'),
    path('purchase/character/', PurchaseCharacter.as_view(), name='purchase_character'),
    path('purchase/quiz/', PurchaseQuiz.as_view(), name='purchase_quiz'),
    path('ranks/', RanksList.as_view(), name='ranks'),
    path('save_user_data/', SaveUserDataView.as_view(), name='save_user_data'),
    path('season_top_leaderboard/', SeasonTopLeaderboard.as_view(), name='season_leaderboard'),
    path('season_list/', SeasonList.as_view(), name='season_list'),
    path('select_character/', SelectCharacter.as_view(), name='select_character'),
    path('super_prize/', SuperPrizeView.as_view(), name='super_prize'),
    path('user_data/', UserDataView.as_view(), name='user_data'),
    path('user_leaderboard_all_season/', UserLeaderboardAllSeasonPosition.as_view(), name='user_leaderboard_all_season'),
    path('user_leaderboard_current_season/', UserLeaderboardCurrentSeasonPosition.as_view(), name='user_leaderboard_current_season'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'game'
