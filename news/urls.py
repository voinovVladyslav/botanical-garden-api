from django.urls import path 

from news import views


urlpatterns = [
    path('', views.get_all_news, name='all_news')
]
