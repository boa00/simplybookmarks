from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("register/", views.register_page, name="register_page"),
    path("login/", views.login_page, name="login_page"),
    path("api/register/", views.register_user, name="register_user"),
    path("api/login/", views.login_user, name="login_user"),
    path("api/user/", views.get_current_user_info, name="current_user_info"),
    path("google_openid/", views.openid_page, name="openid_signin"),
    path("api/opendid_ling_generator/", views.generate_openid_link, name="generate_openid_link"),
]