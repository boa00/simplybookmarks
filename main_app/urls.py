from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views
from .views import CustomTokenObtainPairView

urlpatterns = [
    path("", views.home_page),
    path("register/", views.register_page),
    path("login/", views.login_page),
    path("api/register/", views.register_user),
    path("api/login/", views.login_user),
    path("api/user/", views.get_current_user_info),
    path("google_openid/", views.openid_page),
    path("api/opendid_link_generator/", views.generate_openid_link),

    # JWT auth
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]