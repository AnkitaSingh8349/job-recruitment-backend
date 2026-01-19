# backend/userdashboard/serializers.py
from rest_framework import serializers
from .models import Interview
from django.contrib.auth import get_user_model

User = get_user_model()

class InterviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Interview
        fields = [
            "id", "user_id", "user_email", "role", "scheduled_at",
            "mode", "location", "status", "admin_message", "created_by", "created_at"
        ]
        read_only_fields = ("status", "created_by", "created_at")

class CreateInterviewSerializer(serializers.ModelSerializer):
    # accept user id on creation
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Interview
        fields = ["user_id", "role", "scheduled_at", "mode", "location", "admin_message"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.get(id=user_id)
        request = self.context.get("request")
        created_by = request.user if request else None
        interview = Interview.objects.create(user=user, created_by=created_by, **validated_data)
        return interview
