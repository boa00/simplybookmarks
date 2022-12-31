import requests

from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import (
    RegistrationSerializer, 
    LoginSerializer, 
    UserSerializer,
    OpenIDLinkSerializer,
    CustomTokenObtainPairSerializer
)
from .renderers import UserJSONRenderer
from .google import OpenIDConnectHandler

def home_page(request):
    return render(request, "main_app/home_page.html")


def openid_page(request):
    openid_handler = OpenIDConnectHandler()
    code = request.GET.get("code")
    user_data = openid_handler.get_user_data(code=code)
    print(user_data)
    # if user already exists with such email, create a session for him and update his access_token
    # if user does not exist, create user with id_token info and access_token
    # from id_token: email and name, if name does not exit either fill with None or request to enter it in a pop-up
    return render(request, "main_app/openid_page.html")

class LogInUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
            # immidiately log in
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(request.user, data=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCurrentUserInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class GenerateOpenIDLinkView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OpenIDLinkSerializer

    def get(self, request):
        openid_handler = OpenIDConnectHandler()
        openid_link = openid_handler.generate_openid_link()
        serializer = self.serializer_class(data={"openid_link": openid_link})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
# login with openid 
# redirect to google where you confirm cridentials 
# redirect to separate page which parses GET parameters
# if user already exists