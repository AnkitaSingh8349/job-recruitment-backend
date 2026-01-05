from django.urls import path
from .views import register, login, google_auth

urlpatterns = [
    path("auth/register/", register),
    path("auth/login/", login),
    path("auth/google/", google_auth),
]
