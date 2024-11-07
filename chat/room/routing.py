from django.urls import re_path,path

from .consumers import ChatConsumer

#use path for normal pattern or repath for regext one don;t know the diff b/w the two
websocket_urlpatterns=[
    path('ws/chat/<int:pk>/',ChatConsumer.as_asgi())
]