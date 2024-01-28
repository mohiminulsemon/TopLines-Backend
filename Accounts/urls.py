from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name = 'register'),
    path('activate/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.UserLoginApiView.as_view(), name = 'login'),
    path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
    path('updateProfile/', views.UserProfileUpdateView.as_view(), name = 'updateProfile'),
]