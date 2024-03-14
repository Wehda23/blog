from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    refresh_token_view,
)

urlpatterns = [
    path("", LoginView.as_view(), name="login-reset-view"),
    path("logout", LogoutView.as_view(), name="logout-view"),
    path("register", RegisterView.as_view(), name="register-view"),
    path("refresh", refresh_token_view, name="refresh-token-view"),
]
