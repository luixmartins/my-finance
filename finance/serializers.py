from django.contrib.auth.models import User 
from django.db import IntegrityError 

from rest_framework import serializers 

from finance.models import MemberCategoryModel, CategoryModel 

class CategorySerializer(serializers.Serializer): 
    username = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)

    def create(self, data): 
        user = User.objects.get(username=data['username'])
        name = data['name']
        
        category, created = CategoryModel.objects.get_or_create(name=name)
        
        try: 
            MemberCategoryModel.objects.create(member=user, category=category)

        except IntegrityError: 
            raise serializers.ValidationError('This category is already associated with the user')

        return category 
    