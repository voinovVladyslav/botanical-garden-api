from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from PIL import Image
import tempfile
import os

from news.models import News
from news.serializers import (
    NewsSerializer,
    NewsDetailSerializer,
)


NEWS_URL = reverse('news:news-list')


def news_detail(news_id):
    return reverse('news:news-detail', args=[news_id])


def create_news(user, **params):
    defaults = {
        'title': 'Default title',
        'context': 'Default context',
        'hashtag': '#hashtag',
    }
    defaults.update(**params)
    news = News.objects.create(user=user, **defaults)
    return news


def image_upload_url(news_id):
    return reverse('news:news-upload-image', args=[news_id])


class PublicNewsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword123',
        )

    def test_retrieve_news(self):
        create_news(self.user)
        create_news(self.user)

        res = self.client.get(NEWS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        news = News.objects.all().order_by('-id')
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_news_detail(self):
        news = create_news(self.user)
        url = news_detail(news.id)
        res = self.client.get(url)
        serializer = NewsDetailSerializer(news)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_post_not_allowed(self):
        res = self.client.post(NEWS_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_not_allowed(self):
        res = self.client.put(NEWS_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserNewsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_news(self):
        create_news(self.user, title='Title1')
        create_news(self.user, title='Title2')

        res = self.client.get(NEWS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        news = News.objects.all().order_by('-id')
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_post_not_allowed(self):
        res = self.client.post(NEWS_URL, {})

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class ManagerNewsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_manager(
            email='test@example.com',
            password='testpassword123',
        )
        self.client.force_authenticate(self.user)

    def test_create_news(self):
        data = {
            'title': 'Title',
            'context': 'Context',
            'hashtag': '#tag',
        }

        res = self.client.post(NEWS_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        news = News.objects.get(user=self.user)
        self.assertEqual(news.title, data['title'])

    def test_partial_update(self):
        news = create_news(self.user)
        data = {
            'title': 'New Title',
        }

        url = news_detail(news.id)
        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        news.refresh_from_db()
        for key, value in data.items():
            self.assertEqual(getattr(news, key), value)

    def test_full_update(self):
        news = create_news(self.user)
        data = {
            'title': 'Update title',
            'context': 'Update context',
            'hashtag': '#newtag',
        }

        url = news_detail(news.id)
        res = self.client.put(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        news.refresh_from_db()
        for key, value in data.items():
            self.assertEqual(getattr(news, key), value)
        self.assertEqual(news.user, self.user)

    def test_delete(self):
        news = create_news(self.user)

        url = news_detail(news.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        news = News.objects.filter(user=self.user)
        self.assertFalse(news.exists())


class ImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_manager(
            email='test@example.com',
            password='testpassword123',
        )
        self.client.force_authenticate(self.user)
        self.news = create_news(self.user)

    def tearDown(self):
        self.news.image.delete()

    def test_upload_image(self):
        url = image_upload_url(self.news.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            data = {'image': image_file}
            res = self.client.post(url, data, format='multipart')

        self.news.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.news.image.path))

    def test_upload_not_image(self):
        url = image_upload_url(self.news.id)
        data = {'image': 'not image'}
        res = self.client.post(url, data, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
