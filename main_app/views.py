from django.shortcuts import render
from rest_framework.decorators import (
    api_view, renderer_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .forms import NewUserForm
from .serializer import (
    RegistrationSerializer, 
    LoginSerializer, 
    UserSerializer,
    OpenIDLinkSerializer,
)
from .renderers import UserJSONRenderer
from .google import OpenIDConnectHandler

def home_page(request):
    return render(request, "main_app/home_page.html")


def register_page(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
    return render(request, "main_app/register_page.html")


def login_page(request):
    return render(request, "main_app/login_page.html")


def openid_page(request):
    openid_handler = OpenIDConnectHandler()
    code = request.GET.get("code")
    user_data = openid_handler.get_user_data(code=code)
    print(user_data)
    return render(request, "main_app/openid_page.html")

@api_view(['POST'])
@renderer_classes([UserJSONRenderer])
def register_user(request, *args, **kwargs):
    user = request.data.get('user', {})
    serializer = RegistrationSerializer(data=user)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@renderer_classes([UserJSONRenderer])
def login_user(request, *args, **kwargs):
    user = request.data.get("user", {})
    serializer = LoginSerializer(data=user)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@renderer_classes([UserJSONRenderer])
@permission_classes([IsAuthenticated])
def update_user(request, *args, **kwargs):
    user = request.data.get("user", {})
    serializer = UserSerializer(request.user, data=user, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@renderer_classes([UserJSONRenderer])
@permission_classes([IsAuthenticated])
def get_current_user_info(request, *args, **kwargs):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def generate_openid_link(request, *args, **kwargs):
    openid_handler = OpenIDConnectHandler()
    openid_link = openid_handler.generate_openid_link()
    data = {"openid_link": openid_link}
    serializer = OpenIDLinkSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    