from django.urls import path
from . import views

# /user/excursions/
urlpatterns = [
    path('', views.excursions, name='excursions'),
    path('add/', views.excursion_create, name='excursion_create'),
    path('all', views.excursions_all, name='excursions_all'),
    path('delete/<str:excursions_pk>', views.excursions_delete_page, name='delete_excursion_page'),
    path('delete/<str:excursions_pk>/', views.excursions_delete, name='delete_excursion'),
]