from django.shortcuts import render
from rest_framework import generics, status
from .serializers import CustomUserSerializer, LoginUserSerializer
from rest_framework.response import Response
# Passed IsAuthenticated perms as global config 
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.
class RegisterCustomUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Custom Validation done by the serializer
            # serializer.save()
            # This is expensive. Instead of making a db call return the token and user in the create method 
            #user = CustomUser.objects.get(username=serializer.data['username'])
            #token = Token.objects.get(user=user.id)
            #import pdb; pdb.set_trace()
            # Get the user and token directly from the serializer
            user, token = serializer.save()
            return Response({'username': user.username, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginCustomUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            logged_in_user = authenticate(username=username, password=password)

            if logged_in_user is not None:
                token = Token.objects.get(user=logged_in_user.id)
                return Response({'username': logged_in_user.username, 'token': token.key}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Invalid credentials. Please provide the correct username and password'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # import pdb; pdb.set_trace()
        

    
