from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

# router.register('user-detailsview', views.UserUpdateAPIView, basename='user-detailsview')
# router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    # path('', include(router.urls)),
    path('register/', views.UserRegistration.as_view(), name = 'register'),
    path('activate/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.UserLoginApiView.as_view(), name = 'login'),
    path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
]

urlpatterns += router.urls