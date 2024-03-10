from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Post, Rating
from .serializers import CategorySerializer, PostSerializer, RatingSerializer

from rest_framework.permissions import IsAuthenticated, BasePermission
from django.http import Http404



# class PostList(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.permissions import IsAuthenticated, BasePermission
from django.http import Http404

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the post.
        return obj.author == request.user

from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(author=self.request.user)
        return queryset
    

# class PostDetail(APIView):
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)