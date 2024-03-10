from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import PostList, PostDetail
from .views import PostViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'ratings', RatingViewSet)
# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('posts/', PostList.as_view(),name='posts'),
    # path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('',include(router.urls)),
]
