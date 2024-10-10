from django.urls import path
from rest_framework.authtoken import views
from .views import RegisterCustomUserView, LoginCustomUserView


urlpatterns = [
    path('api_token_auth/', views.obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterCustomUserView.as_view(), name='register'),
    path('login/', LoginCustomUserView.as_view(), name='login')
]