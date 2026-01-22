from rest_framework import serializers
from jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "company_name",
            "location",
            "job_type",
            "description",
            "experience",
            "salary",
            "created_at",
        ]
