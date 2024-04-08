from django.contrib.auth.models import User 
from django.db import IntegrityError 

from rest_framework import serializers 

from finance.models import MemberCategoryModel, CategoryModel 

class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CategoryModel 
        fields = ['name']

    def create(self, validated_data): 
        user = self.context['user']
        category, created = CategoryModel.objects.get_or_create(**validated_data)
        
        try:
            MemberCategoryModel.objects.create(member=user, category=category)
        except IntegrityError: 
            raise serializers.ValidationError('This category is already associated with the user')

        return validated_data