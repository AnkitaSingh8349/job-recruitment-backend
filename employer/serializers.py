from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employer


class EmployerRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(max_length=255)

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This email is already registered. Please login."
            )
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        company_name = validated_data["company_name"]

        # 1️⃣ Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # 🔥 IMPORTANT: Employer = staff
        user.is_staff = True
        user.save()

        # 2️⃣ Create Employer profile
        Employer.objects.get_or_create(
            user=user,
            defaults={"company_name": company_name}
        )

        return user
