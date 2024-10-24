from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.testview,name='home'),
    path('register/',views.UserSignup.as_view(),name='register'),
    path('login/',views.UserLogin.as_view(),name='login'),
    path('logout/',views.UserLogout.as_view(),name='logout'),
    path('profile/<int:pk>/',views.UserProfile.as_view(),name='profile'),
    path('update/<int:pk>/',views.UserUpdate.as_view(),name='update'),
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
