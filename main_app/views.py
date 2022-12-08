from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .forms import NewUserForm
from .serializer import RegistrationSerializer

# Create your views here.
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
def register_user(request, *args, **kwargs):
    serializer = RegistrationSerializer(request.data)
    if serializer.is_valid():
        serializer.create()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)