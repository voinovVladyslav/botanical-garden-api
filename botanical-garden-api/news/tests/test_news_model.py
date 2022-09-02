from django.test import TestCase
from django.contrib.auth import get_user_model

from news.models import News


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
