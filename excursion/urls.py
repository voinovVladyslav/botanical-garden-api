from django.urls import path

from excursion import views

urlpatterns = [
    path('',views.excursions, name='excursions'),
    path('create',views.excursion_create, name='excursion_create'),
    path('<str:pk>/',views.excursion_detail, name='excursion_detail'),
    path('<str:pk>/update',views.excursion_update, name='excursion_update'),
    path('<str:pk>/delete',views.excursion_delete, name='excursion_delete'),
]