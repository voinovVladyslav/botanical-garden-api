from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.register_page, name='registration'),
    path('login', views.login_page, name='login'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('settings/update', views.change_profile, name='update_profile'),
    path('excursions/', include('excursion.urls'))
]