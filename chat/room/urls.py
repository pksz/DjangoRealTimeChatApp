from django.urls import path,re_path
from . import views
#urls 

urlpatterns=[
    path('',views.ChatRoom.as_view(),name='chats'),
    path('<slug:slug>/',views.ChatView.as_view(),name='group'),
    path('private/<slug:slug>/',views.PrivateChatView.as_view(),name='start_private_chat'),
]