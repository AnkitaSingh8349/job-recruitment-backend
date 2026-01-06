from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token
from google.auth.transport import requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import RegisterSerializer


# ==================================================
# ADMIN EMAIL (ONLY ADDITION)
# ==================================================
ADMIN_EMAIL = "ankita@ajxtechnologies.com"


# ==================================================
# REGISTER (email/password)
# ==================================================
@swagger_auto_schema(
    method="post",
    request_body=RegisterSerializer,
    responses={200: "User registered successfully"}
)
@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {  # ✅ ADDED (NO CHANGE TO LOGIC)
                "id": user.id,
                "email": user.email,
                "role": "admin" if user.email == ADMIN_EMAIL else "user"
            }
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================================
# LOGIN (email/password)
# ==================================================
@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, example="user@gmail.com"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, example="123456"),
        },
    ),
    responses={200: "Login successful"}
)
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(username=email, password=password)

    if not user:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {  # ✅ ADDED
            "id": user.id,
            "email": user.email,
            "role": "admin" if user.email == ADMIN_EMAIL else "user"
        }
    })


# ==================================================
# GOOGLE LOGIN / REGISTER
# ==================================================
@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["token"],
        properties={
            "token": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Google ID token"
            ),
        },
    ),
    responses={200: "Google login successful"}
)
@api_view(["POST"])
def google_auth(request):
    token = request.data.get("token")

    if not token:
        return Response(
            {"detail": "Token required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        first_name = idinfo.get("given_name", "")
        last_name = idinfo.get("family_name", "")

        if not email:
            return Response(
                {"detail": "Email not available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "new_user": created,
            "user": {  # ✅ ADDED
                "id": user.id,
                "email": user.email,
                "role": "admin" if user.email == ADMIN_EMAIL else "user"
            }
        })

    except ValueError:
        return Response(
            {"detail": "Invalid Google token"},
            status=status.HTTP_400_BAD_REQUEST
        )
