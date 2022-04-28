from django.urls import path
from . import views

# news/
urlpatterns = [
    path('', views.news_all, name='news_all'),
    path('new', views.create_news, name='create_news'),
    path('<str:news_pk>', views.news_single, name='news_single'),
]