from django.test import TestCase 
from django.contrib.auth.models import User

from user.serializers import AuthenticateSerializer

class LoginUser(TestCase): 
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'testpassword')
    
    def test_authentication_success(self):
        data = {
            'username': 'test',
            'password': 'test@testpassword',
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