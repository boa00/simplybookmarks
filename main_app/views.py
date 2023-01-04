from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import User
from .serializer import (
    RegistrationSerializer, 
    LoginSerializer, 
    UserSerializer,
    UpdateTokensSerializer,
    OpenIDConnectSerializer,
    OpenIDLinkSerializer,
    PasswordResetEmailSerializer,
    PasswordReseSerializer
)
from .renderers import UserJSONRenderer


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
        print(user)
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()            
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
        serializer = self.serializer_class(data={"": ""})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTokensView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UpdateTokensSerializer

    def post(self, request):
        refresh_token = request.data
        serializer = self.serializer_class(data=refresh_token)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpenIDConnectView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OpenIDConnectSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request):
        email = request.data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PasswordResetEmailView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetEmailSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordReseSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)




# forgot password leads to a page where you type in you email and hit submit
# then it directs to another page which says that the email has been sent has been sent
# backend checks if there is a user whith sent email
# if exists, it generates a jwt token and sends email with address url/reset&token=jwt_token
# user enters new password and sends it with Bearer jwt_token from the url 
# update password requires isAuthenticated, it has optional paramter that requires previous password
# if success, log user in and redirect to the home page