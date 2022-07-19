from django.urls import path

from accounts import views

# api/
urlpatterns = [
    path('users/', views.users, name='users'),
    path('users/<str:pk>/', views.user_detail, name='user_detail'),

    path('auth/registration', views.registration, name='registration'),

    path('groups/', views.groups, name='groups'),
    path('groups/<str:pk>/', views.group_detail, name='group_detail'),
    
    path('customers/', views.customers, name='customers'),
    path('customers/<str:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<str:pk>/update', views.customer_update, name='customer_update'),
]
