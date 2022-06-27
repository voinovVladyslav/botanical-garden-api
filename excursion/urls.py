from django.urls import path
from . import views

# /user/excursions/
urlpatterns = [
    path('', views.excursions, name='excursions'),
    path('add/', views.add_excursion, name='add_excursion'),
    path('all', views.excursions_all, name='excursions_all'),
    path('delete/<str:excursions_pk>', views.excursions_delete, name='delete_excursion'),
    path('delete/<str:excursions_pk>/', views.excursions_delete_only, name='delete_excursion_only'),
]