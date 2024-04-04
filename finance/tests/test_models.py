from django.test import TestCase
from django.core.exceptions import ValidationError 
from django.db.utils import IntegrityError

from django.contrib.auth.models import User 

from finance.models import CategoryModel, MemberCategoryModel

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

    def test_unique_together_relationship(self): 
        MemberCategoryModel.objects.create(member=self.user, category=self.category)

        with self.assertRaises(IntegrityError): 
            new_obj = MemberCategoryModel.objects.create(member=self.user, category=self.category)

            new_obj.full_clean()


    