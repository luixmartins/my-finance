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
    
class RegisterUserSerializer(serializers.ModelSerializer): 
    password2 = serializers.CharField(write_only=True)

    class Meta: 
        model = User 
        fields = ['username', 'email', 'password', 'password2']

    def create(self, validated_data): 
        if validated_data['password'] != validated_data['password2']: 
            raise ValidationError('Password does not match.')
        
        if User.objects.filter(email=validated_data['email']).exists(): 
            raise ValidationError('Email already exists.')
        
        account = User(username=validated_data['username'], email=validated_data['email'])

        account.set_password(validated_data['password'])
        account.save()

        return account 
    
