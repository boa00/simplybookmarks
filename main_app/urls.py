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
    PasswordResetView
)

urlpatterns = [    
    path("user/", GetCurrentUserInfoView.as_view()),
    path("user/delete", DeleteUserView.as_view()),

    # auth
    path("register/", RegisterUserView.as_view()),
    path('token/', LogInUserView.as_view()),
    path('token/refresh/', UpdateTokensView.as_view()),
    path("google_openid/", OpenIDConnectView.as_view()),
    path("opendid_link_generator/", GenerateOpenIDLinkView.as_view()),

    # password 
    path("password/reset/email/", PasswordResetEmailView.as_view()),
    path("password/reset/", PasswordResetView.as_view()),
]