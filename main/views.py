from django.shortcuts import render, redirect
from django.views import generic, View   
from django.contrib.auth.models import User 
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import auth 

from main import forms 

class LoginView(View): 
    def get(self, request): 
        context = { 
            'form': forms.AuthUserForm()
        }
        return render(request, 'login.html', context)
    
    def post(self, request): 
        form = forms.AuthUserForm(request, request.POST)

        print(form.is_valid())
        if form.is_valid(): 
            user = form.get_user()

            print(user)
            auth.login(request, user)

            return redirect('finance:home')
        context = {
            'form': form, 
            'message': 'Please, enter with a correct username and password. Note that both fields are case sensitive.'
        }
        print(form.errors.as_data())
        return render(request, 'login.html', context)

def logout(request): 
    auth.logout(request)

    return redirect('main:login')

class RegisterUserView(generic.CreateView):
    template_name = 'create_user.html'
    model = User 
    form_class = forms.UserCreateForm
    success_url = reverse_lazy()
    

    

    

    