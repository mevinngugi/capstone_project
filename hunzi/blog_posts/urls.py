from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostByCategoryView


router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('posts/posts_by_category/<str:category>/', PostByCategoryView.as_view(), name='post_by_category'),
]

urlpatterns += router.urls