from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    UpdateProfile,
    UsersListView,
    UserUpdateProfile,
    HelloView,
)

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path(
        "about-me/<int:pk>/update-profile/",
        UpdateProfile.as_view(),
        name="update-profile",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("users-list/", UsersListView.as_view(), name="users-list"),
    path(
        "users-list/<int:user_id>/user-details/",
        UserUpdateProfile.as_view(),
        name="user-details",
    ),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("foo-var", FooBarView.as_view(), name="foo-bar"),
]
