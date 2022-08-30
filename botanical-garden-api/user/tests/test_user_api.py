from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', res.data)

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

    def test_retrieve_token_success(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Dima',
            'last_name': 'Tsal',
        }
        create_user(**user_data)

        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
        }

        res = self.client.post(TOKEN_URL, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_retrieve_token_wrong_credentials(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Dima',
            'last_name': 'Tsal',
        }
        create_user(**user_data)

        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }

        res = self.client.post(TOKEN_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_update_user_auth_required(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Dima',
            'last_name': 'Tsal',
        }
        create_user(**user_data)

        data = {
            'first_name': 'Pasha',
        }
        res = self.client.patch(ME_URL, data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='First name',
            last_name='Last name',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_profile(self):
        res = self.client.get(ME_URL)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertNotContains(res, 'password')

    def test_post_not_allowed(self):
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile(self):
        data = {
            'first_name': 'New name',
            'password': 'newstrongpass',
        }

        res = self.client.patch(ME_URL, data)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, data['first_name'])
        self.assertTrue(self.user.check_password(data['password']))
