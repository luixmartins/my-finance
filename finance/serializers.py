from django.contrib.auth.models import User 
from django.db import IntegrityError 

from rest_framework import serializers 

from finance.models import MemberCategoryModel, CategoryModel, SpentModel, RecurringSpentModel 

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

class RecurringSpentSerializer(serializers.ModelSerializer):
    spent = SpentSerializer()
    class Meta: 
        model = RecurringSpentModel 
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data): 
        user = self.context['user']
        spent_data = validated_data.pop('spent')
        
        
        category = spent_data.get('category')

        del spent_data['category']
        try:
            category_instance = CategoryModel.objects.get(name=category['name'])
            MemberCategoryModel.objects.get(member=user, category=category_instance)

        except (CategoryModel.DoesNotExist, MemberCategoryModel.DoesNotExist):
            raise serializers.ValidationError(f"The category {category['name'].upper()} does not exist or it isn't associated with the user")
            
        spent = SpentModel.objects.create(member=user, category=category_instance, **spent_data)

        recurring_spent = RecurringSpentModel.objects.create(spent=spent, **validated_data)

        return recurring_spent 
    
    def update(self, instance, validated_data):
        user = self.context['user']
        spent_data = validated_data.pop('spent')
        
        spent = instance.spent 

        instance.period = validated_data.get('period', instance.period)
        instance.last_billing_date = validated_data.get('last_billing_date', instance.last_billing_date)

        spent.description = spent_data.get('description', spent.description)
        spent.value = spent_data.get('value', spent.value)
        spent.date = spent_data.get('date', spent.date)
        

        category = spent_data.get('category', spent.category)

        if spent_data.get('category') != spent.category: 
            try:
                category_instance = CategoryModel.objects.get(name=category['name'])
                MemberCategoryModel.objects.get(member=user, category=category_instance)

            except (CategoryModel.DoesNotExist, MemberCategoryModel.DoesNotExist):
                raise serializers.ValidationError(f"The category {category['name'].upper()} does not exist or it isn't associated with the user")
            
            spent.category = category_instance 

        instance.save()
        spent.save()
        
        return instance