from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Customer

# Create your tests here.
class AccessTest(TestCase):
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

