from django.urls import path 

from contact import views

# api/contacts/
urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('create', views.contact_create, name='contact_create'),
    path('<str:pk>/', views.contact_detail, name='contact_detail'),
    path('<str:pk>/update', views.contact_update, name='contact_update'),
    path('<str:pk>/delete', views.contact_delete, name='contact_delete'),
]
