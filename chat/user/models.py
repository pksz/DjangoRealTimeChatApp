from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    displayname=models.CharField(max_length=20,null=True,blank=True)
    profile_picture=models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    info=models.TextField(null=True,blank=True)
    
   

    def __str__(self) -> str:
        return str(self.user)
    
    @property
    def name(self):
        if self.displayname:
            return str(self.displayname)
        return str(self.user.username)

   #change ?
    @property
    def avatar(self):
        if self.profile_picture:
            return self.profile_picture.url
        return f'{settings.STATIC_URL}images/avatar.svg'