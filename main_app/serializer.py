import os
import secrets
import string

import jwt

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.serializers import ValidationError 

from .models import User, Bookmark
from .utils.tokens import generate_tokens, refresh_token_is_valid
from .utils.google_openid import OpenIDConnectHandler
from .utils.email_sender import send_reset_password_email
from .utils.title_parser import get_page_title


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
        if User.objects.filter(email=validated_data["email"]).exists():
            raise ValidationError("User already exists")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
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
            raise ValidationError("The password is incorrect")
        
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

    openid_link = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        openid_handler = OpenIDConnectHandler()
        openid_link = {
            "openid_link": openid_handler.generate_openid_link()
        }
        return openid_link


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

class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        email = data["email"]

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError("A user with such email does not exist")
        
        user_id = user.pk
        payload_data = {
            "email": email,
            "user_id": user_id,
        }

        tokens = generate_tokens(payload_data)
        send_reset_password_email(jwt_token=tokens["access"], reciever=email)

        return email

class PasswordReseSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=255, required=True)
    old_password_requested = serializers.BooleanField(required=True) 
    old_password = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        email = data["email"]
        new_password = data["new_password"]
        old_password_requested = data["old_password_requested"]
        old_password = data.get("old_password", None)
        
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError("A user with such email does not exist")

        if old_password_requested:
            if old_password is None:
                raise ValidationError("The old password is required")
            if not user.check_password(old_password):
                raise ValidationError("The old password is incorrect")

        if user.check_password(new_password):
            raise ValidationError("The new password is the same as the old one")
        
        user.set_password(new_password)
        user.save()

        return email
            

class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = "__all__"
        read_only_fields = ['user']


class GetPageTitleViewSerializer(serializers.Serializer):
    url = serializers.CharField(required=False)
    title = serializers.CharField(required=False)

    def validate(self, data):
        url = data.get("url", None)
        if url is None:
            raise ValidationError("URL is required")

        title = get_page_title(url)
        
        title_data = {
            "title": title
        }
        
        return title_data
    