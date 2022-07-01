from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import os

from news.models import News
from botanical_garden.settings import BASE_DIR
from excursion.models import Excursion


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

    def test_can_create_excursion(self):
        self.client.post(
            '/',
            data={
                'date': ['2022-07-18'],
                'time': ['11:00'],
                'type': ['Індивідуальні відвідування'],
            }
        )
        excursions = Excursion.objects.count()
        self.assertEqual(excursions, 1)
    
    def test_redirect_after_POST(self):
        response = self.client.post(
            '/',
            data={
                'date': ['2022-07-18'],
                'time': ['11:00'],
                'type': ['Індивідуальні відвідування'],
            }
        )
        self.assertEqual(response.status_code, 302)


class HistoryPageTest(TestCase):
    def test_url_using_right_template(self):
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/history.html')

class StructurePageTest(TestCase):
    def test_url_using_right_template(self):
        response = self.client.get('/structure')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/structure.html')
