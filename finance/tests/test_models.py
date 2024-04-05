from django.test import TestCase
from django.core.exceptions import ValidationError 
from django.db.utils import IntegrityError
from django.contrib.auth.models import User 

import datetime 

from finance.models import CategoryModel, MemberCategoryModel, SpentModel, RecurringSpentModel

class Category(TestCase): 
    def setUp(self): 
        self.category = CategoryModel.objects.create(
            name='Test'
        )

    def test_create_category(self): 
        obj = CategoryModel.objects.create(name='smartphone')

        self.assertIsInstance(obj, CategoryModel)

    def test_create_non_valid_name_category(self): 
        obj = CategoryModel.objects.create(name='T')

        with self.assertRaises(ValidationError): 
            obj.full_clean()

class MemberCategory(TestCase): 
    def setUp(self): 
        self.user = User.objects.create(username='luiz', password='test@test')
        self.category = CategoryModel.objects.create(name='eletronic')
        self.obj = MemberCategoryModel.objects.create(member=self.user, category=self.category)

    def test_create_data(self): 
        obj = MemberCategoryModel.objects.create(member=self.user, category=CategoryModel.objects.create(name='books'))

        self.assertIsInstance(obj, MemberCategoryModel)

    def test_return_created_data(self): 
        self.assertEquals(str(self.obj), 'luiz - eletronic')

    def test_unique_together_relationship(self): 

        with self.assertRaises(IntegrityError): 
            new_obj = MemberCategoryModel.objects.create(member=self.user, category=self.category)

            new_obj.full_clean()

class Spent(TestCase): 
    def setUp(self): 
        self.member = User.objects.create(username='luiz', password='test@test')
        self.category = CategoryModel.objects.create(name='eletronic')
        
        self._  = MemberCategoryModel.objects.create(member=self.member, category=self.category)
    
    def create_spent_without_valid_category_for_user(self): 
        obj_cat = CategoryModel.objects.create(name='home')

        with self.assertRaises(ValidationError): 
            obj = SpentModel.objects.create(
                description='spent on food', 
                value = 98.23, 
                member = self.member, 
                category = obj_cat, 
            )

            obj.full_clean()

    def test_create_spent_without_date_field(self): 
        obj = SpentModel.objects.create(
            description='spent on food', 
            value=152.21, 
            member = self.member, 
            category = self.category, 
        )

        self.assertIsInstance(obj, SpentModel)
    
    def test_create_spent_with_date_field(self): 
        obj = SpentModel.objects.create(
            description='spent on food', 
            value=152.21, 
            date=datetime.date(2024, 4, 2),
            member = self.member, 
            category = self.category,
        )

        self.assertIsInstance(obj, SpentModel)
    
    def test_create_spent_with_negative_value(self): 
        with self.assertRaises(ValidationError): 
            obj = SpentModel.objects.create(
                description='spent on food', 
                value=-15.21, 
                date=datetime.date(2024, 4, 2),
                member = self.member, 
                category = self.category, 
            )
            
            obj.full_clean()

class RecurringSpent(TestCase): 
    def setUp(self): 
        self.member = User.objects.create(username='luiz', password='test@test')
        self.category = CategoryModel.objects.create(name='eletronic')
        _ = MemberCategoryModel.objects.create(member=self.member, category=self.category)
        
        self.spent = SpentModel.objects.create(
            description = 'spent on gpu', 
            value = 947.89, 
            member = self.member, 
            category = self.category, 
        )

    def test_create_invalid_period_for_recurring_spent(self): 
        with self.assertRaises(ValidationError): 
            obj = RecurringSpentModel.objects.create(
                period=-1, 
                spent=self.spent, 
            )

            obj.full_clean()