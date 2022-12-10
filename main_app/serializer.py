from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in")

        if password is None:
            raise serializers.ValidationError("A password is required to log in")
        
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("A user with such password and email does not exist")
        
        user_data = {
            "email": user.email,
            "token": user.token
        }

        return user_data