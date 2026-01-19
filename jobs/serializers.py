from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("id", "created_at", "created_by")
