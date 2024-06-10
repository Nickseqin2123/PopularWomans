from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth import get_user_model


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user1',
            'email': 'bletigri@gmail.com',
            'first_name': 'zxcursed',
            'last_name': 'zzzz',
            'password1': 'ZXCPUDGE1010',
            'password2': 'ZXCPUDGE1010'
        }
    
    def test_form_register_get(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')
        
    def test_user_reg_success(self):
        user_model = get_user_model()
        
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())
    
    def test_error_password(self):
        self.data['password2'] = 'ZXCPUDGE101'
        
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают')
    
    def test_login_error(self):
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')