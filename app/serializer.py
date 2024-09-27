from rest_framework import serializers
from django.contrib.auth.models import User
from .models import React  # Ensure you import the correct model

class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['employee', 'department']  # Ensure these fields exist in the React model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Adjust fields as needed
