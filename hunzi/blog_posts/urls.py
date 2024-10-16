from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostByCategoryView, PostByAuthorView, CommentView, CommentDetailView


router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('posts/posts_by_category/<str:category>/', PostByCategoryView.as_view(), name='post_by_category'),
    path('posts/posts_by_author/<int:id>/', PostByAuthorView.as_view(), name='post_by_author'),
    # Comments
    path('posts/<int:pk>/comments/new/', CommentView.as_view(), name='add_comment'),
    # Read, Update, Delete Comment by ID
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('', PostViewSet.as_view({'get': 'list'}), name='all_posts')
]

urlpatterns += router.urls