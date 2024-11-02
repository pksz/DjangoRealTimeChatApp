from django.forms import ModelForm
from .models import GroupMessage

#

class CreateMessage(ModelForm):
    class Meta:
        model=GroupMessage
        fields=['chat_message']