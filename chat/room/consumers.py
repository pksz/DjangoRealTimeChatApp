from channels.generic.websocket import WebsocketConsumer
import json
from django.shortcuts import get_object_or_404
from .models import Group,GroupMessage
from asgiref.sync import async_to_sync
#

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        
        self.user=self.scope['user']
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.chatroom=get_object_or_404(Group,id=self.room_name)
        
        self.accept()
    

   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]

        self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "user": self.user.username,
                "message": message,
            },
        )


        message=GroupMessage.objects.create(
            group=self.room_name,
            content=message_content,
            author=self.user,   
            
        )

    def disconnect(self, code):
      pass

    
