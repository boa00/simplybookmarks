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
    CustomTokenObtainPairView
)

urlpatterns = [
    path("", views.home_page),
    
    path("api/register/", RegisterUserView.as_view()),
    path("api/login/", LogInUserView.as_view()),
    path("api/user/", GetCurrentUserInfoView.as_view()),

    # JWT auth
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # OpenID 
    path("google_openid/", views.openid_page),
    path("api/opendid_link_generator/", GenerateOpenIDLinkView.as_view()),
]