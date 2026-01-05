from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        email = validated_data["email"]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user
