from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views
from .views import (
    LogInUserView,
    RegisterUserView,
    GetCurrentUserInfoView,
    GenerateOpenIDLinkView,
    CustomTokenObtainPairView,
    UpdateTokensView,
    DeleteUserView,
    OpenIDConnectView,
)

urlpatterns = [
    path("", views.home_page),
    
    path("api/register/", RegisterUserView.as_view()),
    path("api/user/", GetCurrentUserInfoView.as_view()),
    path("api/user/delete", DeleteUserView.as_view()),

    path("api/login/", LogInUserView.as_view()),
    path("api/update_tokens/", UpdateTokensView.as_view()),

    # JWT auth
    path('api/token/', LogInUserView.as_view()),
    path('api/token/refresh/', UpdateTokensView.as_view()),

    # OpenID 
    path("api/google_openid/", OpenIDConnectView.as_view()),
    path("api/opendid_link_generator/", GenerateOpenIDLinkView.as_view()),
]