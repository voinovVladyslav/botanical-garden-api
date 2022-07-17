from django.urls import path 

from news import views

# api/news/
urlpatterns = [
    path('', views.news, name='news'),
    path('<str:pk>/', views.news_detail, name='news_detail'),
]
