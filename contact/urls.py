from django.urls import path, include
from rest_framework import routers

from contact import views


router = routers.DefaultRouter()
router.register(r'contacts', views.ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
