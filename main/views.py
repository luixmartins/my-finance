from django.shortcuts import render
from django.views import generic, View   
from django.contrib.auth.models import User 
from django.urls import reverse_lazy

from main import forms 

class Home(generic.TemplateView): 
    template_name = 'home.html'

class OtherHome(generic.TemplateView): 
    ... 

class RegisterUserView(generic.CreateView):
    template_name = 'create_user.html'
    model = User 
    form_class = forms.UserCreateForm
    success_url = reverse_lazy()
    

    

    

    