from channels.generic.websocket import WebsocketConsumer
import json
from django.shortcuts import get_object_or_404
from .models import Group,GroupMessage
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
#

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        
        self.user=self.scope['user']
        print(self.scope['url_route']['kwargs'])
        self.room_name=self.scope['url_route']['kwargs']['pk']
        self.chatroom=get_object_or_404(Group,id=self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom.group_name,           #need room name as str
            self.channel_name,
          )   
        
        self.accept()
    

   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        msg=text_data_json['chat_message']

        message=GroupMessage.objects.create(        #message added to db
            chat_message=msg,
            author=self.user,
            group=self.chatroom,
        )
        
        #create an event that will trigger on sending message type=function name that will
        #handle the event

        event={
            'type':'message_handler',
            'message':msg,
            'message_id':message.id   

        }

        async_to_sync(self.channel_layer.group_send)(self.chatroom.group_name,event)
        

    def message_handler(self,event):
        #find the message based on msg id / find a faster way
        message_id=event['message_id']
        chatmessage=GroupMessage.objects.get(id=message_id)
        
        #context will be sent to frontend
        context={
            'message':chatmessage,
            'author':self.user
        }
        
        #html=render_to_string('room/group.html',context=context)

        self.send(text_data=json.dumps({'message':chatmessage.chat_message,
            'user': self.user.username}))




    def disconnect(self, code):
     async_to_sync(self.channel_layer.group_discard)(
            self.chatroom.group_name,
            self.channel_name,
            
            
        )

    
