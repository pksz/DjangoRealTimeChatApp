from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,DeleteView
from . models import Group,GroupMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateMessage,CreateChatRoom
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
       # y=Group.objects.get(slug=self.kwargs['slug'])

        #print(y.__dict__)
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



#create new chatroom
class CreateNewChatRoom(LoginRequiredMixin,CreateView):
    model=Group
    form_class=CreateChatRoom
    template_name='room/createnewchatroom.html'

    def form_valid(self, form) -> HttpResponse:
        newgroup=form.save(commit=False)
        newgroup.admin=self.request.user
        newgroup.save()
        newgroup.members.add(self.request.user)
        
        object=newgroup
        
        return redirect('group', slug=object.slug)

    def get_success_url(self):
        # Redirect to the object detail page by its slug
        return reverse_lazy('group', kwargs={'slug': self.object.slug})


#delete chatrooms 
class DeleteChatroom(LoginRequiredMixin,DeleteView):
    model=Group
    success_url=reverse_lazy('chatroom')



#handles private message b/w users and redirects to new group
class PrivateChat(LoginRequiredMixin,View):  
    model=Group
    private_chatroom_name=''
    #create a new group if none exist should be post request
    def get(self, request,**kwargs: Any) -> dict[str, Any]:
        private_chatroom_name=self.request.user.username+self.kwargs['slug']

        private_chatroom,created=Group.objects.get_or_create(group_name=private_chatroom_name,
                                                             defaults={'group_description':f'{self.request.user.username}{self.kwargs['slug']} group',
                                                                       'slug':slugify(private_chatroom_name),
                                                                       'is_private':True})
        

        if created:
            private_chatroom.members.add(self.request.user)
            private_chatroom.members.add(User.objects.get(username=self.kwargs['slug']))
            private_chatroom.save()


        #context= super().get_context_data(**kwargs)
        context={}
        print(private_chatroom.pk)
        context['sent_chats']=GroupMessage.objects.filter(group=private_chatroom.pk)
        context['form']=CreateMessage()
        context['room_name']=Group.objects.get(slug=private_chatroom.slug)
        context['pk']=private_chatroom.pk
          

        print(private_chatroom.group_name)
        return redirect('group',slug=private_chatroom.slug)
        #return render(request,'room/privatechat.html',context=context)




   
    
    


    

    

