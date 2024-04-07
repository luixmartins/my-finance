from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers 
from rest_framework.exceptions import ValidationError

class AuthenticateSerializer(serializers.Serializer): 
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    def validate(self, data): 
        username = data.get('username')
        password = data.get('password')
 
        user = authenticate(username=username, password=password)
            
        if user: 
            return {'user': user}
        
        raise ValidationError('Invalid credentials')
            