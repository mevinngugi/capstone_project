from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
import django_filters
from .permissions import IsAuthorOrReadOnly


# Custom filters that returns partial search on the title and author name
class PostListFilter(django_filters.FilterSet):
    published_date = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ('published_date', 'category')


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
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
