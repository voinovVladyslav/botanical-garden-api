from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_successfully(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Dima',
            'last_name': 'Tsal',
        }

        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, 'email')
        self.assertContains(res, 'first_name')
        self.assertContains(res, 'last_name')
        self.assertNotContains(res, 'password')

    def test_create_user_error(self):
        data = {
            'email': '',
            'password': 'testpassword123',
            'first_name': 'Dima',
            'last_name': 'Tsal',
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short(self):
        data = {
            'email': 'test@example.com',
            'password': 'test',
            'first_name': 'Dima',
            'last_name': 'Tsal',
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=data['email']).exists()
        self.assertFalse(user_exists)

    def test_create_user_email_already_used(self):
        email = 'test@example.com'
        create_user(email=email, password='testpassword123')
        data = {
            'email': email,
            'password': 'testpassword123',
            'first_name': 'Dima',
            'last_name': 'Tsal',
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
