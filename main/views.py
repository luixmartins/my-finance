from django.shortcuts import render, redirect
from django.views import generic, View   
from django.contrib.auth.models import User 
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import auth 

from main import forms 

class Home(View): 
    def get(self, request): 
        context = { 
            'form': forms.AuthUserForm()
        }
        return render(request, 'login.html', context)
    
    def post(self, request): 
        form = forms.AuthUserForm(request, self.request.POST)

        if form.is_valid(): 
            user = form.get_user()

            auth.login(request, user)

            return redirect('finance:home')
        context = {
            'form': form 
        }

        return render(request, 'home.html', context)


class RegisterUserView(generic.CreateView):
    template_name = 'create_user.html'
    model = User 
    form_class = forms.UserCreateForm
    success_url = reverse_lazy()
    

    

    

    