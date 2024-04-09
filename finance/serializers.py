from django.contrib.auth.models import User 
from django.db import IntegrityError 

from rest_framework import serializers 

from finance.models import MemberCategoryModel, CategoryModel, SpentModel

class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CategoryModel 
        fields = ['id', 'name']
        
        read_only_fields = ['id']


    def create(self, validated_data): 
        user = self.context['user']
        category, created = CategoryModel.objects.get_or_create(**validated_data)
        
        try:
            MemberCategoryModel.objects.create(member=user, category=category)
        except IntegrityError: 
            raise serializers.ValidationError('This category is already associated with the user')

        return validated_data
    
class SpentSerializer(serializers.ModelSerializer): 
    category  = serializers.CharField(source='category.name')
    value = serializers.DecimalField(decimal_places=2, max_digits=10)

    class Meta: 
        model = SpentModel 
        read_only_fields = ['id']
        exclude = ['member']

    def create(self, validated_data): 
        validated_data['member'] = self.context['user']
        category = validated_data['category']['name']

        
        try: 
            validated_data['category'] = CategoryModel.objects.get(name=category)
            
            MemberCategoryModel.objects.get_or_create(member=validated_data['member'], category=validated_data['category'])

        except CategoryModel.DoesNotExist: 
            raise serializers.ValidationError(f'The category does not exists.')
         
        return SpentModel.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        user = self.context['user']

        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.value = validated_data.get('value', instance.value)
        
        category_data = validated_data.get('category')
        if category_data:
            category_name = category_data.get('name')
            
            try:
                category_instance = CategoryModel.objects.get(name=category_name)
                MemberCategoryModel.objects.get(member=user, category=category_instance)

            except (CategoryModel.DoesNotExist, MemberCategoryModel.DoesNotExist):
                raise serializers.ValidationError("The category does not exist or it isn't associated with the user")
                
            instance.category = category_instance

        instance.save()

        return instance