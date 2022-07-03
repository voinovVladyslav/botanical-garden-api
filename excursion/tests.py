from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from accounts.models import Customer
from .models import Excursion


class UserExcursionsPageTest(TestCase):
    def tearDown(self):
        self.client.logout()
        
    def loginUser(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='pasha',
            email='default@gmail.com',
            password='pavlik135'
        )
        Customer.objects.create(user=self.user)
        self.client.force_login(self.user)

    def loginManager(self):
        User = get_user_model()
        group = Group.objects.get_or_create(name='manager')
        self.manager = User.objects.create(
            username='manager',
            email='default@gmail.com',
            password='pavlik135',
        )
        self.manager.groups.set(group)
        Customer.objects.create(user=self.manager)
        
        self.client.force_login(self.manager)


    def test_anonymuos_user_redirect_to_login_page(self):
        response = self.client.get('/user/excursions/')
        self.assertEqual(response.status_code, 302)

    def test_authorised_user_access_granted(self):
        self.loginUser()
        response = self.client.get('/user/excursions/')
        self.assertEqual(response.status_code, 200)
