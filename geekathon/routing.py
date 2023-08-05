from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/globalchat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/game/(?P<playerid>\w+)/(?P<roomname>\w+)/(?P<playername>\w+)/(?P<oname>\w+)/$', consumers.GameConsumer.as_asgi()),
]