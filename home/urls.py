from django.contrib import admin
from django.urls import path
from .import views
from .views import google_login_callback 
#home
urlpatterns = [
    path('',views.home),
    path('comming_soon/',views.comingsoon),
    path('settings/',views.settings),
    path('reset/',views.reset),
    path('logout/',views.logout_now),
    path('leaderboard/',views.leaderboard, name='leaderboard'),
    path('accounts/google/login/callback/', google_login_callback, name='google_login_callback'),
    path('matchmaking/',views.matchup,name='matchup'),
    path('join-game/', views.join_game, name='join_game'),
    path('join-global/',views.join_global , name="join_global"),
    path('game/', views.game_view, name='game_view'),
    path('mid/',views.mid,name='mid'),
    path('rank/',views.rerank,name='rank'),
    path('delete-matchmaking/',views.delmatch,name='delmatch'),
    path('update_score/', views.update_score, name='update_score'),
    path('surrender_score/',views.surrender_score,name='surrender_score'),
    path('left_score/',views.left_score,name="left_score"),
    path('permanentdelete/',views.perm_delete,name='acc deltion'),
    path('suggest/',views.suggest,name='suggest'),
    path('globalchat/',views.chat_view,name='globalchat'),
    path('gchatmid/',views.gchatmid,name='gchatmid')
]
