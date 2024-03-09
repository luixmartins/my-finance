from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  

class UserCreateForm(UserCreationForm): 
    username = forms.CharField(label='Username', min_length=5, max_length=150, label_suffix='', 
                               widget=forms.TextInput(attrs={
                                    'class': 'form-control', 
                                    'id': 'usernameInput', 
                                }))

    password1 = forms.CharField(label='Password', label_suffix='', 
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control', 
                                    'id': 'passwordInput', 
                                }))
    
    password2 = forms.CharField(label='Confirm password',  label_suffix='', 
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control', 
                                    'id': 'passwordInput', 
                                }))
    
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        user = User.objects.filter(username = username)  
        
        if user.count():  
            raise ValidationError("User Already Exist")  
        return username  
    
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        
        elif len(password1) < 8: 
            raise ValidationError("Your password must contain at least 8 characters.")  
        
        elif password1.isnumeric(): 
            raise ValidationError("Your password cannot be entirely numbers.")

        return password2  
    
    def save(self, commit = True):  
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']

        user = User.objects.create_user(  
            username = username, 
            password = password
        )  
        return user  

    

        