from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from news.models import Hashtag
from news.serializers import HashtagSerializer


HASHTAG_URL = reverse('news:hashtag-list')


def create_hashtag(name='#testhashtag'):
    return Hashtag.objects.create(name=name)

class HashtagApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_hashtags(self):
        create_hashtag()
        create_hashtag('#new')

        res = self.client.get(HASHTAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        hashtags = Hashtag.objects.all()
        serializer = HashtagSerializer(hashtags, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_hashtag(self):
        data = {'name': '#name'}

        res = self.client.post(HASHTAG_URL, data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ManagerApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_manager(
            email='test@example.com',
            password='testpassword123',
        )
        self.client.force_authenticate(self.user)

    def test_create_hashtag(self):
        data = {'name': '#name'}

        res = self.client.post(HASHTAG_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        hashtag = Hashtag.objects.filter(name=data['name'])
        self.assertTrue(hashtag.exists())
