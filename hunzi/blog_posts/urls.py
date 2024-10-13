from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostByCategoryView, PostByAuthorView


router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('posts/posts_by_category/<str:category>/', PostByCategoryView.as_view(), name='post_by_category'),
    path('posts/posts_by_author/<int:id>/', PostByAuthorView.as_view(), name='post_by_author'),
]

urlpatterns += router.urls