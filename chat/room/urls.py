from django.urls import path,re_path
from . import views
#urls 

urlpatterns=[
    path('newgroup/',views.CreateNewChatRoom.as_view(),name='newgroup'),
    path('',views.ChatRoom.as_view(),name='chats'),
    path('<slug:slug>/',views.ChatView.as_view(),name='group'),
    path('private/<slug:slug>/',views.PrivateChat.as_view(),name='start_private_chat'),
    
]