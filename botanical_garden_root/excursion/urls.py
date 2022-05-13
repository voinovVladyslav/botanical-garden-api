from django.urls import path
from . import views

# /user/excursions/
urlpatterns = [
    path('', views.excursions, name='excursions'),
    path('delete/<str:excursions_pk>', views.excursions_delete, name='delete_excursion'),
]