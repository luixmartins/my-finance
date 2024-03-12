from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 

@method_decorator(login_required(login_url='main:login'), name='dispatch')
class HomeView(generic.TemplateView):
    template_name = 'home.html'  

