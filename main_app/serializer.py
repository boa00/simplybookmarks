import os
import secrets
import string

import jwt

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ValidationError 

from .models import User
from .utils.tokens import generate_tokens, refresh_token_is_valid
from .google import OpenIDConnectHandler

class RegistrationSerializer(serializers.ModelSerializer):
    # add password checks and return errors if needed
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    # return errors as data if needed
    email = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=128, write_only=True, required=False)
    access = serializers.CharField(max_length=255, required=False)
    refresh = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise ValidationError("An email address is required to log in")

        if password is None:
            raise ValidationError("A password is required to log in")

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError("A user with such email does not exist")

        if not user.check_password(password):
            raise ValidationError("A user with such password and email does not exist")
        
        payload_data = {
            "email": user.email,
            "user_id": user.id,
        }

        tokens = generate_tokens(payload_data=payload_data)

        return tokens


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None: 
            instance.set_password(password)

        instance.save()
        return instance

class OpenIDLinkSerializer(serializers.Serializer):

    openid_link = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class UpdateTokensSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255, required=True)
    access = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        if not refresh_token_is_valid(data["refresh"]):
            raise ValidationError("Refresh token is not valid")

        token_decoded = jwt.decode(data["refresh"], os.environ["SECRET_KEY"], algorithms=["HS256"])
        payload_data = {
            "email": token_decoded["email"],
            "user_id": token_decoded["user_id"],
        }
        tokens = generate_tokens(payload_data=payload_data)
        return tokens


class OpenIDConnectSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255, required=False)
    refresh = serializers.CharField(max_length=255, required=False)
    access = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        code = data.get("code", None)

        if code is None:
            raise ValidationError("Code for OpenID connect was not provided")

        openid_handler = OpenIDConnectHandler()
        user_data = openid_handler.get_user_data(code=code)
        email = user_data["email"]

        if User.objects.filter(email=email).exists():
            user_id = User.objects.get(email=email).pk
        else:
            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(secrets.choice(alphabet) for i in range(25))  
            new_user_data = {
                "email": email,
                "password": password
            }
            user = User.objects.create_user(**new_user_data)
            user_id = user.pk

        
        payload_data = {
            "email": email,
            "user_id": user_id,
        }

        tokens = generate_tokens(payload_data=payload_data)

        return tokens
