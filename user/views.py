from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated

from user.serializers import AuthenticateSerializer

class LoginView(APIView): 
    def post(self, request): 
        serializer = AuthenticateSerializer(data=request.POST)

        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            
            response = {
                'token': str(Token.objects.get_or_create(user=user)[0])
            }

            return Response(response, status=status.HTTP_202_ACCEPTED)
        
        return Response({'Authorization': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
    
class LogoutView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)
    
class RegisterView(APIView): 
    ... 