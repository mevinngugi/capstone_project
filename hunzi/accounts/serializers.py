from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


class CustomUserSerializer(serializers.ModelSerializer):
    # Validation using Charfield
    username = serializers.CharField(min_length=3, max_length=50, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        # Pass the fields you want to be converted to json
        fields = ['username', 'email', 'password']


    # Pass in validation for the custom user 
    def validate(self, data):
        #import pdb; pdb.set_trace()
        filter_for_existing_username = CustomUser.objects.filter(username=data['username']).exists()
        if filter_for_existing_username:
            raise serializers.ValidationError({'username': 'Username must be unique.'})
        
        # TODO consider using regex to validate emails and usernames     
        if '@gmail.com' not in data['email']:
            raise serializers.ValidationError({'email': 'Please enter a valid gmail email address.'})

        filter_for_existing_email = CustomUser.objects.filter(email=data['email']).exists()
        if filter_for_existing_email:
            raise serializers.ValidationError({'email': 'Email must be unique.'})
            
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        # Create token every time a new user is created.                
        token = Token.objects.create(user=user)
        # TODO Send welcome email from here or use django signals 
        return user, token


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)

    def validate(self, data):
        # Check if username exist but if it does not don't tell the user that it does not exists
        get_object_or_404(CustomUser, username=data['username'])
        return data

