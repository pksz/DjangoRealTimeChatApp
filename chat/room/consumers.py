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
        self.room_name=self.scope['url_route']['kwargs']['pk']
        self.chatroom=get_object_or_404(Group,id=self.room_name)

        #add group to websocket
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom.group_name,           #need room name as str
            self.channel_name,
          )    
        

        #check for online user status
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()
    

   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

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
            'action':"send_message",
            'message':msg,
            'message_id':message.id   

        }
        # to all groups
        async_to_sync(self.channel_layer.group_send)(self.chatroom.group_name,event)
        

    def message_handler(self,event):
        #find the message based on msg id / find a faster way
        message_id=event['message_id']
        chatmessage=GroupMessage.objects.get(id=message_id)
        
        #context will be sent to frontend
        context={
            'message':chatmessage.chat_message,
            'action': 'send_message',
            'user':self.user.username
        }
        
        #~~html=render_to_string('room/group.html',context=context)~~

        #frontend updates the current page by using this data
        self.send(text_data=json.dumps(context))




    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom.group_name, #needs it in str
            self.channel_name)

        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()


    def update_online_count(self):
        online_count=0
        online_count=self.chatroom.users_online.count() - 1
        event={
            'type':'online_count_handler',
            'action':'online_user_update',
            'online_count':online_count
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom.group_name,event)

    
    def online_count_handler(self,event):
        online_count=event['online_count']
        print(online_count)
        self.send(text_data=json.dumps({'action':'online_user_update','online_count':online_count}))
