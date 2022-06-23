from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('thanks/', views.thanks, name='thanks'),
    path('all/', views.contact_all, name='contact_all'),
    path('<str:contact_pk>/', views.contact_single, name='contact_single'),
]