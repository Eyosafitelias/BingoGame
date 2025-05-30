# a_ygame/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bingo/card-selection/(?P<room_name>\w+)/$', consumers.CardSelectionConsumer.as_asgi()),
    re_path(r'ws/bingo/game/(?P<room_name>\w+)/$', consumers.GameConsumer.as_asgi()),
]
