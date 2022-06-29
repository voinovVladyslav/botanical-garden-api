from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.contrib.auth import login

from accounts.models import Customer


class LogInUsers():
    def create_default_user(self):
        user = User.objects.create(
            username='default_user',
            email='default@gmail.com',
            password1='django1357',
            password2='django1357'
        )

        group = Group.objects.get(name='customer')
        user.groups.add(group)
        
        Customer.objects.create(user=user)
        self.user = user

    def login_default_user(self):
        login(self.user)


class ContactPageTest(TestCase):
    def test_url_using_right_template(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')


class SubmitContactPage(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/contact/submit/')
        self.assertEqual(response.status_code, 302) 
