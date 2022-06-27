from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registerPage, name='registration'),
    path('registration/register/', views.registerUser, name='register_user'),
    path('login', views.loginPage, name='login'),
    path('login/', views.loginUser, name='login_user'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('settings/update', views.change_profile, name='update_profile'),
    path('excursions/', include('excursion.urls'))
]