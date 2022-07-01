from django.test import TestCase
from django.contrib.auth import get_user_model


class ContactPageTest(TestCase):
    def test_url_using_right_template(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')


class SubmitContactPage(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='default_user', email='default@gmail.com', password='default_password')
