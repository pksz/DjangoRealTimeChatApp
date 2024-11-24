from django.forms import ModelForm
from .models import GroupMessage,Group

#

class CreateMessage(ModelForm):
    class Meta:
        model=GroupMessage
        fields=['chat_message']


class CreateChatRoom(ModelForm):

    class Meta:
        model=Group
        fields=['group_name']