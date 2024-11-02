from typing import Any
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from . models import Group,GroupMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateMessage
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse_lazy
# Create your views here.

class ChatRoom(LoginRequiredMixin,ListView):
    model=Group
    template_name='room/chatrooms.html'


class ChatGroup(LoginRequiredMixin,DetailView):
    model=Group
    template_name='room/group.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        context['sent_chats']=GroupMessage.objects.filter(group=self.object)
        context['form']=CreateMessage()
        return context



class ChatForm(SingleObjectMixin, FormView):
    template_name = "room/group.html"
    form_class = CreateMessage
    model = GroupMessage
    success_url='#'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
       # self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    

    def form_valid(self, form):
     post = self.get_object()
     myform = form.save(commit=False)
     #variales here
     myform.author =  self.request.user  
     myform.group = Group.objects.get(id=self.kwargs['pk'])
     form.save()
     return super(ChatForm, self).form_valid(form)
    
    

class ChatView(LoginRequiredMixin,View):
  def get(self, request, *args, **kwargs):
      view = ChatGroup.as_view()
      return view(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
      view = ChatForm.as_view()

      #msg=CreateMessage(request.POST)
      #msg.instance.author = request.user
      #msg.instance.group=Group.objects.get(id=self.kwargs['pk'])
      

      #if msg.is_valid():
           # msg.save(   )
      return view(request, *args, **kwargs)