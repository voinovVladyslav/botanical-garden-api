from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from PIL import Image
import tempfile
import os
from datetime import date, timedelta

from news.models import News, Hashtag
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

    def test_news_filter_by_date_gte(self):
        news1 = create_news(self.user, title='News1')
        news2 = create_news(self.user, title='News2')
        news3 = create_news(self.user, title='News3')
        yesterday = date.today() - timedelta(days=1)
        news3.publication_date = yesterday
        news3.save()

        params = {'publication_date_gte': f'{news1.publication_date}'}
        res = self.client.get(NEWS_URL, params)

        s1 = NewsSerializer(news1)
        s2 = NewsSerializer(news2)
        s3 = NewsSerializer(news3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

    def test_news_filter_by_date_lte(self):
        news1 = create_news(self.user, title='News1')
        news2 = create_news(self.user, title='News2')
        news3 = create_news(self.user, title='News3')
        yesterday = date.today() - timedelta(days=1)
        news3.publication_date = yesterday
        news3.save()

        params = {'publication_date_lte': f'{news3.publication_date}'}
        res = self.client.get(NEWS_URL, params)

        s1 = NewsSerializer(news1)
        s2 = NewsSerializer(news2)
        s3 = NewsSerializer(news3)

        self.assertNotIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
        self.assertIn(s3.data, res.data)

    def test_news_filter_by_gte_and_lte(self):
        news1 = create_news(self.user, title='News1')
        news2 = create_news(self.user, title='News2')
        news3 = create_news(self.user, title='News3')
        news4 = create_news(self.user, title='News4')

        news1.publication_date = date.today()
        news2.publication_date = date.today() - timedelta(days=2)
        news3.publication_date = date.today() - timedelta(days=5)
        news4.publication_date = date.today() - timedelta(days=8)

        news1.save()
        news2.save()
        news3.save()
        news4.save()

        params = {
            'publication_date_gte': f'{news3.publication_date}',
            'publication_date_lte': f'{news2.publication_date}',
        }
        res = self.client.get(NEWS_URL, params)

        s1 = NewsSerializer(news1)
        s2 = NewsSerializer(news2)
        s3 = NewsSerializer(news3)
        s4 = NewsSerializer(news4)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertIn(s3.data, res.data)
        self.assertNotIn(s4.data, res.data)

    def test_news_fiter_by_hashtag(self):
        news1 = create_news(self.user, title='News1')
        news2 = create_news(self.user, title='News2')
        news3 = create_news(self.user, title='News3')
        hashtag1 = Hashtag.objects.create(name='#hashtag1')
        hashtag2 = Hashtag.objects.create(name='#hashtag2')
        news1.hashtags.add(hashtag1)
        news2.hashtags.add(hashtag2)

        params = {'hashtags': f'{hashtag1.id}'}
        res = self.client.get(NEWS_URL, params)

        s1 = NewsSerializer(news1)
        s2 = NewsSerializer(news2)
        s3 = NewsSerializer(news3)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

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
            'hashtags': [{'name': '#news2'}],
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

    def test_create_news_with_new_hashtags(self):
        data = {
            'title': 'title',
            'context': 'context',
            'hashtags': [{'name': '#hashtag1'}, {'name': '#hashtag2'}],
        }

        res = self.client.post(NEWS_URL, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        news = News.objects.filter(user=self.user)
        self.assertEqual(news.count(), 1)
        news = news[0]
        self.assertEqual(news.hashtags.count(), 2)

        for hashtag in data['hashtags']:
            exists = news.hashtags.filter(
                name=hashtag['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_news_with_existing_hashtags(self):
        Hashtag.objects.create(name='#hashtag1')
        data = {
            'title': 'title',
            'context': 'context',
            'hashtags': [{'name': '#hashtag1'}, {'name': '#hashtag2'}],
        }

        res = self.client.post(NEWS_URL, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        news = News.objects.filter(user=self.user)
        self.assertEqual(news.count(), 1)
        news = news[0]
        self.assertEqual(news.hashtags.count(), 2)

        for hashtag in data['hashtags']:
            exists = news.hashtags.filter(
                name=hashtag['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_hashtags_on_update(self):
        news = create_news(self.user)
        data = {'hashtags': [{'name': '#newtag'}]}
        url = news_detail(news.id)
        res = self.client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_hashtag = Hashtag.objects.get(name='#newtag')
        self.assertIn(new_hashtag, news.hashtags.all())

    def test_assign_hashtag_on_update(self):
        hashtag = Hashtag.objects.create(name='#hashtag')
        news = create_news(self.user)
        news.hashtags.add(hashtag)

        new_hashtag = Hashtag.objects.create(name='#newhashtag')
        data = {'hashtags': [{'name': '#newhashtag'}]}
        url = news_detail(news.id)
        res = self.client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(new_hashtag, news.hashtags.all())
        self.assertNotIn(hashtag, news.hashtags.all())

    def test_clear_news_hashtags(self):
        hashtag = Hashtag.objects.create(name='#news')
        news = create_news(self.user)
        news.hashtags.add(hashtag)

        data = {'hashtags': []}
        url = news_detail(news.id)
        res = self.client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(news.hashtags.count(), 0)


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
