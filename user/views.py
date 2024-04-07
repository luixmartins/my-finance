from django.contrib.auth.models import User 

from rest_framework.views import APIView 
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated

from user.serializers import AuthenticateSerializer, RegisterUserSerializer

class LoginView(APIView): 
    def post(self, request): 
        serializer = AuthenticateSerializer(data=request.POST)

        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            
            token, created = Token.objects.get_or_create(user=user)
            
            response = {
                'token': token.key
            }

            return Response(response, status=status.HTTP_202_ACCEPTED)
        
        return Response({'Authorization': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
    
class LogoutView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)
    
class RegisterView(generics.CreateAPIView): 
    serializer_class = RegisterUserSerializer 

    def create(self, request): 
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = User.objects.get(username=serializer.data['username'])
        token, created = Token.objects.get_or_create(user=user)
                
        data = serializer.data 
        data['token'] = token.key 

        return Response(data, status.HTTP_201_CREATED)