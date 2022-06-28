from tkinter import W
from django.test import TestCase
from news.models import News
from django.core.files.uploadedfile import SimpleUploadedFile
from botanical_garden.settings import BASE_DIR
import os

# Create your tests here.
class HomePageTest(TestCase):
    def create_news_objects(self, news_title):
        test_img_path = os.path.join(BASE_DIR, 'botanical_garden/static/test_img/welcome-cat.jpg')
        news = News.objects.create(
            title=news_title,
            context='context1',
            hashtag='#hashtag1',
            preview=SimpleUploadedFile(
                name='tree.jpg', 
                content=open(test_img_path, 'rb').read(),
                content_type='image/jpeg'
            )
        )
        return news

    def test_url_using_right_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/main.html')

    def test_page_displays_news(self):
        news1 = self.create_news_objects('title1')
        news2 = self.create_news_objects('title2')

        response = self.client.get('/')

        self.assertContains(response, news1)
        self.assertContains(response, news2)
        
    def test_displays_two_latest_news(self):
        news1 = self.create_news_objects('title1')
        news2 = self.create_news_objects('title2')
        news3 = self.create_news_objects('title3')
        
        response = self.client.get('/')

        self.assertNotContains(response, news1)
        self.assertContains(response, news2)
        self.assertContains(response, news3)
