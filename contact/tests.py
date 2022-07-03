from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

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


class AllContactPageTest(TestCase):
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
        self.user = User.objects.create(
            username='manager',
            email='default@gmail.com',
            password='pavlik135',
        )
        self.user.groups.set(group)
        Customer.objects.create(user=self.user)
        
        self.client.force_login(self.user)

    def test_unauthorised_user_permision_denied(self):
        response = self.client.get('/contact/all')
        self.assertEqual(response.status_code, 403)

    def test_default_user_permision_denied(self):
        self.loginUser()
        response = self.client.get('/contact/all')
        self.assertEqual(response.status_code, 403)

    def test_manager_permision_granted(self):
        self.loginManager()
        response = self.client.get('/contact/all')
        self.assertEqual(response.status_code, 200)

    def test_page_contains_contact_messages(self):
        self.loginManager()
        contact1 = Contact.objects.create(topic='topic1', message='message1')
        contact2 = Contact.objects.create(topic='topic2', message='message2')

        response = self.client.get('/contact/all')

        self.assertContains(response, contact1)
        self.assertContains(response, contact2)


class ContactSinglePageTest(TestCase):
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
        self.user = User.objects.create(
            username='manager',
            email='default@gmail.com',
            password='pavlik135',
        )
        self.user.groups.set(group)
        Customer.objects.create(user=self.user)
        
        self.client.force_login(self.user)

    def test_unauthorised_user_permision_denied(self):
        response = self.client.get('/contact/1')
        self.assertEqual(response.status_code, 403)

    def test_default_user_permision_denied(self):
        self.loginUser()
        response = self.client.get('/contact/1')
        self.assertEqual(response.status_code, 403)

    def test_manager_permision_granted(self):
        contact = Contact.objects.create(topic='manager_topic', message='manager_message')
        self.loginManager()
        response = self.client.get(f'/contact/{contact.id}')
        self.assertEqual(response.status_code, 200)

    def test_page_contains_only_one_message(self):
        self.loginManager()
        contact1 = Contact.objects.create(topic='topic1', message='message1')
        contact2 = Contact.objects.create(topic='topic2', message='message2')

        response = self.client.get(f'/contact/{contact1.id}')

        self.assertContains(response, contact1)
        self.assertNotContains(response, contact2)
    