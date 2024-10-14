from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
import django_filters
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostListFilter(django_filters.FilterSet):
    """Custom filters that returns partial search on the title and author name.g"""
    published_date = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ('published_date', 'category')


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    """A viewSet for the Post Model."""
    # Because you are overriding the permission classes in settings.py
    # You need to pass in the IsAuthenticatedOrReadOnly to prevent
    # unauthenticated users from attempting to create a post
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostListFilter
    search_fields = ['title', 'content', 'author']
    ordering_fields = ['title', 'created_date']
    # Default ordering 
    ordering = ['created_date']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostByCategoryView(generics.GenericAPIView):
    """A view that returns the posts grouped by category."""
    model = Post

    def get(self, request, category):
        #import pdb; pdb.set_trace()
        post_categories = ['Tutorial', 'Project', 'Deployment']
        if category not in post_categories:
            return Response({'error': f'The category must be one of the following: \'{', '.join(post_categories)}\''})
        
        post_by_category = Post.objects.filter(category=category)
        if post_by_category.exists():
            serializer = PostSerializer(post_by_category, many=True)
            return Response(serializer.data)
        return Response(f'No posts have been under the category {category}')


class PostByAuthorView(generics.GenericAPIView):
    """A view that return the posts grouped by author."""
    model = Post

    def get(self, request, id):
        #import pdb; pdb.set_trace()
        author = get_object_or_404(CustomUser, id=id)
        post_by_author = Post.objects.filter(author=author)
        if post_by_author:
            serializer = PostSerializer(post_by_author, many=True)
            return Response(serializer.data)
        return Response('You have not yet created any posts')


class CommentView(generics.CreateAPIView):
    """A view to create a comment and attach it to a post"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        # import pdb; pdb.set_trace()
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """A view to Get, Put, Patch, Delete a comment."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
