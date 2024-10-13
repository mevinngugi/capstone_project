from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Post
from .serializers import PostSerializer
import django_filters
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response


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


class PostByCategoryView(generics.GenericAPIView):
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
