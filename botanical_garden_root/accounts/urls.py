from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registerPage, name='registration'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('excursions/', include('excursion.urls'))
]