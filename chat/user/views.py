from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import FormView,ListView,DetailView,UpdateView
from django.contrib.auth.views import LoginView,LogoutView
from.forms import UserSignUpForm,UserProfileUpdate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Profile
# Create your views here.

def testview(request):
    return render(request,'user/base.html')

class UserSignup(FormView):
    form_class=UserSignUpForm
    template_name='user/registration.html'
    success_url=reverse_lazy('home')
    
    def form_valid(self, form):
    
        user=form.save()
        if user is not None:
            login(self.request,user)

        return super(UserSignup,self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(UserSignup,self).get(request, *args, **kwargs)


   

class UserLogin(LoginView):
    template_name="user/login.html"
    redirect_authenticated_user=True
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')


class UserLogout(LoginRequiredMixin,LogoutView):
    template_name="user/logout.html"
    next_page=reverse_lazy('home')


class UserProfile(LoginRequiredMixin,DetailView):
    model =Profile
    template_name='user/profile.html'



class UserUpdate(LoginRequiredMixin,UpdateView):
    model=Profile
    fields=[
        'displayname',
            'profile_picture',
            'info',
    ]
    
    template_name='user/profile_update.html'


    success_url=reverse_lazy('home')

   



