from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch

from news.models import News, news_image_file_path


class NewsModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_manager(
            email='test@example.com',
            password='testpassword234',
        )

    def test_create_news(self):
        News.objects.create(
            title='News title',
            context='News context',
            hashtag='#news',
            user=self.user,
        )

        news = News.objects.get(user=self.user)
        self.assertEqual(news.title, 'News title')
        self.assertEqual(news.context, 'News context')
        self.assertEqual(str(news), news.title)

    @patch('news.models.uuid.uuid4')
    def test_image_upload(self, patched_uuid4):
        uuid = 'test-uuid-name'
        patched_uuid4.return_value = uuid
        file_path = news_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/news/{uuid}.jpg')
