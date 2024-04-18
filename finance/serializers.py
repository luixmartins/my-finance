from django.contrib.auth.models import User 
from django.db import IntegrityError 
from django.db.models import Q 

from rest_framework import serializers 

from finance.models import  CategoryModel, SpentModel

from user.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer): 

    class Meta: 
        model = CategoryModel
        exclude = ['user']
        read_only_fields = ['id']

    def create(self, validated_data): 
        user = self.context['user']

        try: 
            category = CategoryModel.objects.create(user=user, **validated_data)
        except IntegrityError: 
            raise serializers.ValidationError("This category is already associated with the user.")
        
        return category 
    
class SpentSerializer(serializers.ModelSerializer): 
    category = CategorySerializer()
    value = serializers.DecimalField(decimal_places=2, max_digits=10)
    
    class Meta: 
        model = SpentModel 
        exclude = ['user']
        read_only_fields = ['id']

    def create(self, validated_data): 
        user = self.context['user']
        name = validated_data.pop('category')['name']


        if CategoryModel.objects.filter(user=user, name=name).exists(): 
            category = CategoryModel.objects.get(user=user, name=name)
        else: 
            category = CategoryModel.objects.create(user=user, name=name)
    
        spent = SpentModel.objects.create(category=category, user=user, **validated_data)

        return spent 
    
    def update(self, instance, validated_data): 
        user = self.context['user']
        
        recurring = validated_data.get('recurring', instance.recurring)

        if recurring is False and recurring != instance.recurring:
            spents_recurring = SpentModel.objects.filter(
                Q(
                    user = user, 
                    value = instance.value, 
                    description = instance.description, 
                    period = instance.period, 
                    recurring = True
                )
            ) 

            for spent in spents_recurring: 
                spent.recurring = False
                spent.period = None
                
                spent.save()
            
            instance.recurring = False 
        else:
            instance.recurring = True  


        instance.value = validated_data.get('value', instance.value)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.period = validated_data.get('period', instance.period)
        
        category_data = validated_data.get('category', instance.category)

        if not isinstance(category_data, CategoryModel) and category_data != None: 
            name = category_data.get('name')
            try: 
                category_instance = CategoryModel.objects.get(user=user, name=name)
            except: 
                category_instance = CategoryModel.objects.create(user=user, name=name)
            
            instance.category = category_instance

        instance.save()

        return instance 
#     def update(self, instance, validated_data):
#         user = self.context['user']

#         instance.date = validated_data.get('date', instance.date)
#         instance.description = validated_data.get('description', instance.description)
#         instance.value = validated_data.get('value', instance.value)
        
#         category_data = validated_data.get('category')
#         if category_data:
#             category_name = category_data.get('name')
            
#             try:
#                 category_instance = CategoryModel.objects.get(name=category_name)
#                 MemberCategoryModel.objects.get(member=user, category=category_instance)

#             except (CategoryModel.DoesNotExist, MemberCategoryModel.DoesNotExist):
#                 raise serializers.ValidationError("The category does not exist or it isn't associated with the user")
                
#             instance.category = category_instance

#         instance.save()

#         return instance

# class RecurringSpentSerializer(serializers.ModelSerializer):
#     spent = SpentSerializer()
#     class Meta: 
#         model = RecurringSpentModel 
#         fields = '__all__'
#         read_only_fields = ['id']

#     def create(self, validated_data): 
#         user = self.context['user']
#         spent_data = validated_data.pop('spent')
        
        
#         category = spent_data.get('category')

#         del spent_data['category']
#         try:
#             category_instance = CategoryModel.objects.get(name=category['name'])
#             MemberCategoryModel.objects.get(member=user, category=category_instance)

#         except (CategoryModel.DoesNotExist, MemberCategoryModel.DoesNotExist):
#             raise serializers.ValidationError(f"The category {category['name'].upper()} does not exist or it isn't associated with the user")
            
#         spent = SpentModel.objects.create(member=user, category=category_instance, **spent_data)

#         recurring_spent = RecurringSpentModel.objects.create(spent=spent, **validated_data)

#         return recurring_spent 
    
#     def update(self, instance, validated_data):
#         user = self.context['user']
#         spent_data = validated_data.pop('spent')
        
#         spent = instance.spent 

#         instance.period = validated_data.get('period', instance.period)
#         instance.last_billing_date = validated_data.get('last_billing_date', instance.last_billing_date)

#         spent.description = spent_data.get('description', spent.description)
#         spent.value = spent_data.get('value', spent.value)
#         spent.date = spent_data.get('date', spent.date)
        

#         category = spent_data.get('category', spent.category)

#         if spent_data.get('category') != spent.category: 
#             try:
#                 category_instance = CategoryModel.objects.get(name=category['name'])
#                 MemberCategoryModel.objects.get(member=user, category=category_instance)

#             except (CategoryModel.DoesNotExist, MemberCategoryModel.DoesNotExist):
#                 raise serializers.ValidationError(f"The category {category['name'].upper()} does not exist or it isn't associated with the user")
            
#             spent.category = category_instance 

#         instance.save()
#         spent.save()
        
#         return instance