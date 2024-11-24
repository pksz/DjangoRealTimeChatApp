from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
# Create your models here.

class Group(models.Model):
    group_name=models.CharField(max_length=40,default=uuid.uuid4,unique=True)
    group_description=models.TextField(blank=True,null=True)
    users_online=models.ManyToManyField(User,related_name='online_in_group',blank=True)
    members=models.ManyToManyField(User,related_name='members',blank=True)
    admin=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    is_private=models.BooleanField(default=False)
    #optional
    #group_icon= models.ImageField(blank=True,null=True)
    slug=models.SlugField(unique=True,blank=True)
    #unique_field(group_name+created_by)

    def __str__(self) -> str:
        return self.group_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.group_name)  # Automatically generate the slug based on the group name
        super().save(*args, **kwargs)


class GroupMessage(models.Model): #like posts
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    chat_message=models.CharField(max_length=300)
    chat_timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.author} : {self.chat_message}'
    

    class Meta:
        ordering=['-chat_timestamp']


  
