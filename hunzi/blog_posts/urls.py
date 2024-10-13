from rest_framework.routers import DefaultRouter
from .views import PostViewSet


router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = []

urlpatterns += router.urls