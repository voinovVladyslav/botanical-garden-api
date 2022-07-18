from django.urls import path 

from contact import views



urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('<str:pk>/', views.contact_detail, name='contact_detail'),
]
