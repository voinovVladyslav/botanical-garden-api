from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Customer
from .models import Contact


class ContactPageTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='pasha',
            email='default@gmail.com',
            password='pavlik135'
        )
        Customer.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_url_using_right_template(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_redirect_after_post(self):
        response = self.client.post(
            '/contact/submit/',
            {'topic':'my_topic', 'message':'my_message'}
        )
        self.assertRedirects(response, '/contact/thanks')


class SubmitContactPageTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            username='pasha',
            email='default@gmail.com',
            password='pavlik135'
        )
        Customer.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_404_when_get_request(self):
        response = self.client.get('/contact/submit/')
        self.assertEqual(response.status_code, 404)
        
    def test_create_contact_object(self):
        self.client.post(
            '/contact/submit/',
            {'topic':'my_topic', 'message':'my_message'}
        )
        count = Contact.objects.count()
        contact = Contact.objects.first()
        
        self.assertEqual(count, 1)
        self.assertEqual(contact.topic, 'my_topic')

    def test_redirect_after_POST(self):
        response = self.client.post(
            '/contact/submit/',
            {'topic':'my_topic', 'message':'my_message'}
        )
        self.assertRedirects(response, '/contact/thanks')
        

class ThanksPageTest(TestCase):
    def test_page_using_right_template(self):
        response = self.client.get('/contact/thanks')
        self.assertTemplateUsed(response, 'contact/thanks.html')
