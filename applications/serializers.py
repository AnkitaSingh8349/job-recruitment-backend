from rest_framework import serializers
from jobs.models import Application


# ===============================
# CREATE APPLICATION (USER SIDE)
# ===============================
class ApplicationCreateSerializer(serializers.ModelSerializer):
    # Optional from frontend
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Application
        fields = [
            "job",
            "full_name",
            "email",
            "phone",
            "experience_years",
            "expected_salary",
            "preferred_technology",
            "cover_letter",
        ]

    def create(self, validated_data):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")

        # ✅ Assign logged-in user
        validated_data["user"] = request.user

        # ✅ Auto-fill name & email from user
        validated_data["full_name"] = (
            validated_data.get("full_name")
            or request.user.get_full_name()
        )

        validated_data["email"] = (
            validated_data.get("email")
            or request.user.email
        )

        return Application.objects.create(**validated_data)


# ======================================
# APPLICATION LIST (ADMIN + USER VIEW)
# ======================================
class ApplicationSerializer(serializers.ModelSerializer):
    # 🔑 VERY IMPORTANT (FOR INTERVIEW INVITE)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    user_name = serializers.CharField(source="full_name", read_only=True)
    user_email = serializers.EmailField(source="email", read_only=True)
    phone = serializers.CharField(read_only=True)

    experience = serializers.IntegerField(
        source="experience_years", read_only=True
    )

    technologies = serializers.CharField(
        source="preferred_technology", read_only=True
    )

    job_title = serializers.CharField(
        source="job.title", read_only=True
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "user_id",        # ✅ REQUIRED FOR EMAIL / INTERVIEW
            "user_name",
            "user_email",
            "phone",
            "experience",
            "technologies",
            "job_title",
            "status",
            "admin_message",
            "created_at",
        ]
