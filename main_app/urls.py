from django.urls import path

from .views import (
    LogInUserView,
    RegisterUserView,
    GetCurrentUserInfoView,
    GenerateOpenIDLinkView,
    UpdateTokensView,
    DeleteUserView,
    OpenIDConnectView,
    PasswordResetEmailView,
    PasswordResetView,
    BookmarkListCreateView,
    BookmarkRetrieveUpdateDestroyView,
    GetPageTitleView,
    TagListCreateView,
    TagRetrieveUpdateDestroyView,
)

urlpatterns = [    
    path("user/", GetCurrentUserInfoView.as_view()),
    path("user/delete/", DeleteUserView.as_view()),

    # auth
    path("register/", RegisterUserView.as_view()),
    path('token/', LogInUserView.as_view()),
    path('token/refresh/', UpdateTokensView.as_view()),
    path("google-openid/", OpenIDConnectView.as_view()),
    path("opendid-link-generator/", GenerateOpenIDLinkView.as_view()),

    # password 
    path("password/reset/email/", PasswordResetEmailView.as_view()),
    path("password/reset/", PasswordResetView.as_view()),

    # bookmarks
    path("bookmarks/", BookmarkListCreateView.as_view()),
    path("bookmarks/<int:pk>/", BookmarkRetrieveUpdateDestroyView.as_view()),
    path("bookmarks/tags/", TagListCreateView.as_view()),
    path("bookmarks/tags/<int:pk>/", TagRetrieveUpdateDestroyView.as_view()),

    # utils 
    path("external-title/", GetPageTitleView.as_view()),
]