from unittest            import mock

from django.contrib.auth import get_user_model
from rest_framework      import status
from rest_framework.test import APITestCase

from .models             import User


class RegisterUsertView(APITestCase):
    def setUp(self):
            get_user_model().objects.create_user(
                email    = 'jiwon222@wanted.com',
                password = '12345678',
                name = '유저생성'
            )

    def tearDown(self):
        User.objects.all().delete()

    def test_create_user_success(self):
        data = {
            "email"    : "jiwon111@wanted.com",
            "password" : "password123@",
            "name"     : "지원"
        }
        response = self.client.post('/users/signup/', data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_existed_mail_error(self):
        data = {
            "email"    : "jiwon222@wanted.com",
            "password" : "password123@",
            "name"     : "지원"
        }
        response = self.client.post('/users/signup/', data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_mail_error(self):
        data = {
            "email"    : "jjjjj",
            "password" : "password123@",
            "name"     : "지원"
        }
        response = self.client.post('/users/signup/', data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_name_error(self):
        data = {
            "email"    : "jjjjj",
            "password" : "password123@",
            "name"     : ""
        }
        response = self.client.post('/users/signup/', data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginView(APITestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            email    = 'jiwon222@wanted.com',
            password = '12345678',
            name     = '유저생성'
        ) 

    def tearDown(self):
        User.objects.all().delete()

    def test_login_success(self):
        data = {
            "email"    : "jiwon222@wanted.com",
            "password" : "12345678",
        }
        response = self.client.post('/users/login/', data = data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_password_fail(self):
        data = {
            "email"    : "jiwon222@wanted.com",
            "password" : "12345",
        }
        response = self.client.post('/users/login/', data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)