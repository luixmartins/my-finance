from django.test import TestCase 
from django.contrib.auth.models import User

from rest_framework.exceptions import ValidationError

from user.serializers import AuthenticateSerializer, RegisterUserSerializer

class LoginUser(TestCase): 
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'testpassword')
    
    def test_authentication_success(self):
        data = {
            'username': 'test',
            'password': 'testpassword',
        }
        serializer = AuthenticateSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)

    def test_authentication_failure(self):
        data = {
            'username': 'test',
            'password': 'wrongpassword',
        }
        serializer = AuthenticateSerializer(data=data)

        self.assertFalse(serializer.is_valid())

class RegisterSerializer(TestCase): 
    def setUp(self): 
        self.data = { 
            'username': 'test',
            'email': 'email@test.com', 
            'password': 'admin', 
            'password2': 'admin'
        }

        self.user = User.objects.create(username='test2', email='test@test.com', password='admin')

    def test_create_valid_user(self): 
        serializer = RegisterUserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        
        if serializer.is_valid(): 
            response = serializer.save()
            self.assertIsInstance(response, User)

    def test_create_invalid_email_user(self): 
        self.data['email'] = 'test@test.com'

        serializer = RegisterUserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        with self.assertRaises(ValidationError): 
            serializer.save()

    def test_create_invalid_password_user(self): 
        self.data['password2'] = 'test'

        serializer = RegisterUserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        with self.assertRaises(ValidationError): 
            serializer.save()