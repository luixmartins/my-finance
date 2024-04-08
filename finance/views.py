from django.contrib.auth.models import User 

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from finance.serializers import CategorySerializer
from finance.models import MemberCategoryModel, CategoryModel

class CategoryListCreateView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request): 
        categories = CategoryModel.objects.filter(category__member=request.user)
        
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)
        
    
    def post(self, request): 
        serializer = CategorySerializer(data=request.POST, context={'user': request.user})

        if serializer.is_valid(): 
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)