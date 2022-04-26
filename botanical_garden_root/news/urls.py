from django.urls import path
from . import views

# news/
urlpatterns = [
    path('all', views.news_all, name='news_all'),
    path('<str:news_pk>', views.news_single, name='news_single'),
]