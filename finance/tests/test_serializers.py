from django.test import TestCase 
from django.contrib.auth.models import User 

from finance.serializers import CategorySerializer
from finance.models import CategoryModel

class CategoryTest(TestCase): 
    def setUp(self): 
        self.user = User.objects.create_user('test', 'test@email.com', 'testpassword')

        data = {
            'username': self.user.username, 
            'name': 'eletronic'
        }
        serializer = CategorySerializer(data=data)
        
        if serializer.is_valid(): 
            self.response = serializer.save()
    
    def test_serializer(self): 
        user = User.objects.create_user('luiz', 'luiz@test.com', 'testpassword')
        data = {
            'username': user.username, 
            'name': 'eletronic'
        }

        serializer = CategorySerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        
        response = serializer.save()

        self.assertIsInstance(response, CategoryModel)

