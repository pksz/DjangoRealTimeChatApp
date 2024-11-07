from channels.generic.websocket import WebsocketConsumer
import json
from django.shortcuts import get_object_or_404
from .models import Group,GroupMessage
from asgiref.sync import async_to_sync
#

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        
        self.user=self.scope['user']
        print(self.scope['url_route']['kwargs'])
        self.room_name=self.scope['url_route']['kwargs']['pk']
        self.chatroom=get_object_or_404(Group,id=self.room_name)
        
        async_to_sync(self.channel_layer.group_add(
            self.channel_name,
            self.chatroom,
        ))
       
        self.accept()
    

   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        msg=text_data_json['chat_message']

        message=GroupMessage.objects.create(
            chat_message=msg,
            author=self.user,
            group=self.chatroom,
        )
        
        async_to_sync(self.channel_layer.group_send(self.chatroom,message))

       

    def disconnect(self, code):
      pass

    
