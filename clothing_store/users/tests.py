from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterUserTests(TestCase):

    def test_register_user(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_existing_username(self):
        User.objects.create_user(username='testuser', password='testpassword123')
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')
