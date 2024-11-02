from django.urls import path,re_path
from . import views
#urls 

urlpatterns=[
    path('',views.ChatRoom.as_view(),name='chats'),
    path('<str:pk>/',views.ChatView.as_view(),name='group'),
]