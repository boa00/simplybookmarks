from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status

from .forms import NewUserForm
from .serializer import RegistrationSerializer, LoginSerializer
from .renderers import UserJSONRenderer

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
    