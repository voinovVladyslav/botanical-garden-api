from django.urls import path 

from news import views

# api/news/
urlpatterns = [
    path('', views.news, name='news'),
    path('create', views.news_create, name='news_create'),
    path('<str:pk>/', views.news_detail, name='news_detail'),
    path('<str:pk>/update', views.news_update, name='news_update'),
    path('<str:pk>/delete', views.news_delete, name='news_delete'),
]
