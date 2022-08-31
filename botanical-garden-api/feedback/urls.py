from rest_framework.routers import DefaultRouter

from django.urls import path, include

from feedback import views


router = DefaultRouter()
router.register('reviews', views.ReviewViewSet)
router.register('all-reviews', views.ReviewGlobalViewSet, basename='all-review')


app_name = 'feedback'


urlpatterns = [
    path('', include(router.urls)),
]
