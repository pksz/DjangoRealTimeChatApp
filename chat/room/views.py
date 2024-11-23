from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,TemplateView
from . models import Group,GroupMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateMessage
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your views here.
#lists public chatrooms
class ChatRoom(LoginRequiredMixin,ListView):
    model=Group
    template_name='room/chatrooms.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset=Group.objects.all().filter(is_private=False)
        return queryset


#public chatroom view
class ChatGroup(LoginRequiredMixin,DetailView):
    model=Group
    template_name='room/group.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        context['sent_chats']=GroupMessage.objects.filter(group=self.object)
        context['form']=CreateMessage()
        context['room_name']=Group.objects.get(slug =self.kwargs['slug'])
        y=Group.objects.get(slug=self.kwargs['slug'])

        print(y.__dict__)
        return context



class ChatForm(SingleObjectMixin, FormView):
    template_name = "room/group.html"
    form_class = CreateMessage
    model = GroupMessage
    success_url='#'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        return super().post(request, *args, **kwargs)
    

    def form_valid(self, form):
     print('valid')
     print(self.kwargs['slug'])
     myform = form.save(commit=False)
     #variales here
     myform.author =  self.request.user  
     myform.group = Group.objects.get(slug=self.kwargs['slug'])
     form.save()
     return super(ChatForm, self).form_valid(form)
    
    

class ChatView(LoginRequiredMixin,View):
  def get(self, request, *args, **kwargs):
      view = ChatGroup.as_view()
      return view(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
      view = ChatForm.as_view()
      return view(request, *args, **kwargs)



#handles private message b/w users
class PrivateChat(LoginRequiredMixin,View):  
    model=Group
    private_chatroom_name=''
    #create anew group if none exist
    def get(self, request,**kwargs: Any) -> dict[str, Any]:
        private_chatroom_name=self.request.user.username+self.kwargs['slug']
        print(private_chatroom_name)

        private_chatroom,created=Group.objects.get_or_create(group_name=private_chatroom_name,
                                                             defaults={'group_description':f'{self.request.user.username}{self.kwargs['slug']} group',
                                                                       'slug':slugify(private_chatroom_name),
                                                                       'is_private':True})
        

        if created:
            private_chatroom.members.add(self.request.user)
            private_chatroom.members.add(User.objects.get(username=self.kwargs['slug']))
            private_chatroom.save()


        #context= super().get_context_data(**kwargs)
       # context['sent_chats']=GroupMessage.objects.filter(group=self.object)
       # context['form']=CreateMessage()
        #context['room_name']=Group.objects.get(slug =self.kwargs['slug'])
           

        print(private_chatroom)
        return render(request,'room/privatechat.html',{'context':context})
    
    
class PrivateChatView(LoginRequiredMixin,View):
  def get(self, request, *args, **kwargs):
      view = PrivateChat.as_view()
      return view(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
      view = ChatForm.as_view()
      return view(request, *args, **kwargs)

    

    

