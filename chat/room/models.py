from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Group(models.Model):
    group_name=models.CharField(max_length=40)
    group_description=models.TextField(blank=True,null=True)
    #optional
    #group_icon= models.ImageField(blank=True,null=True)
    #slug=models.SlugField()

    def __str__(self) -> str:
        return self.group_name


class GroupMessage(models.Model): #like posts
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    chat_message=models.CharField(max_length=300)
    chat_timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.author} : {self.chat_message}'
    

    class Meta:
        ordering=['-chat_timestamp']


  
