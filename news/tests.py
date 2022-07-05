from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os

from news.models import News
from botanical_garden.settings import BASE_DIR
from accounts.models import Customer


class NewsAllPageTest(TestCase):
    def create_news_objects(self, news_title):
        test_img_path = os.path.join(BASE_DIR, 'botanical_garden/static/test_img/welcome-cat.jpg')
        news = News.objects.create(
            title=news_title,
            context='context1',
            hashtag='#hashtag1',
            image=SimpleUploadedFile(
                name='tree.jpg', 
                content=open(test_img_path, 'rb').read(),
                content_type='image/jpeg'
            )
        )
        return news

    def test_page_displays_all_news(self):
        news1 = self.create_news_objects('title1')
        news2 = self.create_news_objects('title2')
        response = self.client.get('/news/')
        
        self.assertContains(response, news1)
        self.assertContains(response, news2)


class PermissionsTest(TestCase):
    def create_news_objects(self, news_title):
        test_img_path = os.path.join(BASE_DIR, 'botanical_garden/static/test_img/welcome-cat.jpg')
        news = News.objects.create(
            title=news_title,
            context='context1',
            hashtag='#hashtag1',
            image=SimpleUploadedFile(
                name='tree.jpg', 
                content=open(test_img_path, 'rb').read(),
                content_type='image/jpeg'
            )
        )
        return news

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

        
    def test_anonymous_user_access(self):
        news1 = self.create_news_objects('title1')
        all_news_response = self.client.get('/news/')
        single_news_response = self.client.get(f'/news/{news1.id}')
        create_news_response = self.client.get('/news/new')
        update_news_response = self.client.get(f'/news/update/{news1.id}')
        delete_news_response = self.client.get(f'/news/delete/{news1.id}')
        
        self.assertEqual(all_news_response.status_code, 200)
        self.assertEqual(single_news_response.status_code, 200)
        self.assertEqual(create_news_response.status_code, 403)
        self.assertEqual(update_news_response.status_code, 403)
        self.assertEqual(delete_news_response.status_code, 403)

    def test_user_access(self):
        news1 = self.create_news_objects('title1')
        self.loginUser()
        all_news_response = self.client.get('/news/')
        single_news_response = self.client.get(f'/news/{news1.id}')
        create_news_response = self.client.get('/news/new')
        update_news_response = self.client.get(f'/news/update/{news1.id}')
        delete_news_response = self.client.get(f'/news/delete/{news1.id}')
        
        self.assertEqual(all_news_response.status_code, 200)
        self.assertEqual(single_news_response.status_code, 200)
        self.assertEqual(create_news_response.status_code, 403)
        self.assertEqual(update_news_response.status_code, 403)
        self.assertEqual(delete_news_response.status_code, 403)

    def test_manager_access(self):
        news1 = self.create_news_objects('title1')
        self.loginManager()
        all_news_response = self.client.get('/news/')
        single_news_response = self.client.get(f'/news/{news1.id}')
        create_news_response = self.client.get('/news/new')
        update_news_response = self.client.get(f'/news/update/{news1.id}')
        delete_news_response = self.client.get(f'/news/delete/{news1.id}')
        
        self.assertEqual(all_news_response.status_code, 200)
        self.assertEqual(single_news_response.status_code, 200)
        self.assertEqual(create_news_response.status_code, 200)
        self.assertEqual(update_news_response.status_code, 200)
        self.assertEqual(delete_news_response.status_code, 200)
