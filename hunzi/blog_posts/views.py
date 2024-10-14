from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from .models import Post
from .serializers import PostSerializer
import django_filters
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Custom filters that returns partial search on the title and author name
class PostListFilter(django_filters.FilterSet):
    published_date = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ('published_date', 'category')


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
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
    model = Post

    def get(self, request, id):
        #import pdb; pdb.set_trace()
        author = get_object_or_404(CustomUser, id=id)
        post_by_author = Post.objects.filter(author=author)
        if post_by_author:
            serializer = PostSerializer(post_by_author, many=True)
            return Response(serializer.data)
        return Response('You have not yet created any posts')
        