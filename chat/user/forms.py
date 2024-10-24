from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from.models import Profile
#

class UserSignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            'username',
            'password1',
            'password2',
        ]

class UserProfileUpdate(UserChangeForm):
    class Meta:
        model=Profile
        fields=[
            'displayname',
            'profile_picture',
            'info',
        ]
