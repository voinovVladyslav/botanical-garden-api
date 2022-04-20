from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('history', views.history, name='history'),
    path('structure', views.structure, name='structure'),
]