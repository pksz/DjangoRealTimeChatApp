from channels.generic.websocket import WebsocketConsumer
import json
from django.shortcuts import get_object_or_404
#

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        
        username=self.scope['user']
        #self.room_name=self.scope['url_route']['kwargs']['room_name']
        #self.chatroom=get_object_or_404()

        self.channel_layer.group_add()
        self.accept()
    

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))

    
