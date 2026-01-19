from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token
from google.auth.transport import requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import RegisterSerializer
from employer.models import Employer   # ✅ IMPORTANT IMPORT


# ==================================================
# ADMIN EMAIL (FROM settings.py)
# ==================================================
ADMIN_EMAIL = settings.ADMIN_EMAIL


# ==================================================
# REGISTER (NORMAL USER)
# ==================================================
@swagger_auto_schema(
    method="post",
    request_body=RegisterSerializer,
    responses={201: "User registered successfully"}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        # determine role (frontend routing) but keep flags authoritative
        role = "admin" if user.email == ADMIN_EMAIL else "user"

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": role,
                # Added flags for frontend + future checks
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================================
# LOGIN (EMAIL / PASSWORD)  ✅ FIXED
# ==================================================
@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={200: "Login successful"}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"detail": "Email and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=email, password=password)

    if not user:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # ✅ EMPLOYER CHECK (MAIN FIX)
    is_employer = Employer.objects.filter(user=user).exists()

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "email": user.email,
            "role": (
                "admin"
                if user.email == ADMIN_EMAIL
                else "employer"
                if is_employer
                else "user"
            ),
            # Added flags for frontend + authoritative checks
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
    }, status=status.HTTP_200_OK)


# ==================================================
# GOOGLE LOGIN / REGISTER  ✅ FIXED
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
@permission_classes([AllowAny])
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

        # ✅ EMPLOYER CHECK HERE ALSO
        is_employer = Employer.objects.filter(user=user).exists()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "new_user": created,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": (
                    "admin"
                    if user.email == ADMIN_EMAIL
                    else "employer"
                    if is_employer
                    else "user"
                ),
                # Added flags for frontend + authoritative checks
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response(
            {"detail": "Invalid Google token"},
            status=status.HTTP_400_BAD_REQUEST
        )
