from django.urls import path, include
from rest_framework import routers

from accounts import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
