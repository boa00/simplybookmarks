from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import User, Bookmark, Tag
from .serializer import (
    RegistrationSerializer, 
    LoginSerializer, 
    UserSerializer,
    UpdateTokensSerializer,
    OpenIDConnectSerializer,
    OpenIDLinkSerializer,
    PasswordResetEmailSerializer,
    PasswordReseSerializer,
    BookmarkSerializer,
    GetPageTitleViewSerializer,
    TagSerializer
)
from .renderers import UserJSONRenderer


class LogInUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request) -> Response:
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request) -> Response:
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def post(self, request) -> Response:
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

    def get(self, request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class GenerateOpenIDLinkView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OpenIDLinkSerializer

    def get(self, request) -> Response:
        serializer = self.serializer_class(data={"": ""})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTokensView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UpdateTokensSerializer

    def post(self, request) -> Response:
        refresh_token = request.data
        serializer = self.serializer_class(data=refresh_token)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpenIDConnectView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OpenIDConnectSerializer

    def post(self, request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request) -> Response:
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

    def post(self, request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordReseSerializer

    def post(self, request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

class BookmarkListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = (
            Bookmark
            .objects
            .filter_user(user=self.request.user)
            .filter_tags(tag=self.request.query_params.get('tag', None))
            .search(query=self.request.query_params.get('query', None))
            .sort(order=self.request.query_params.get('order', None))
        )
        return queryset


class BookmarkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.all().filter(user=user)


class TagListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return Tag.objects.all().filter(user=user)


class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Tag.objects.all().filter(user=user)

class GetPageTitleView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetPageTitleViewSerializer

    def post(self, request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
