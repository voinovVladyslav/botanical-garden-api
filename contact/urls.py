from django.urls import path
from . import views

# contact/
urlpatterns = [
    path('', views.contact, name='contact'),
    path('submit/', views.contact_submit, name='contact_submit'),
    path('thanks', views.thanks, name='thanks'),
    path('all', views.contact_all, name='contact_all'),
    path('<str:contact_pk>', views.contact_single, name='contact_single'),
]
