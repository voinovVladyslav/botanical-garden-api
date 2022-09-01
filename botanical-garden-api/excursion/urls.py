from django.urls import path, include

from rest_framework.routers import DefaultRouter

from excursion import views

router = DefaultRouter()
router.register('excursions', views.ExcursionViewSet)


app_name = 'excursion'


urlpatterns = [
    path('', include(router.urls)),
]
