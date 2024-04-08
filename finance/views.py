from django.contrib.auth.models import User 

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from finance.serializers import CategorySerializer
from finance.models import MemberCategoryModel 

class CategoryCreateView(APIView): 
    permission_classes = [IsAuthenticated]
    
    def post(self, request): 
        data = {
            'username': request.user.username, 
            'name': request.POST['name']
        }
        
        serializer = CategorySerializer(data=data)

        if serializer.is_valid(): 
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)