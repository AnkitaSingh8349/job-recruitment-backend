from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.conf import settings
from urllib.parse import quote

from .models import Job
from .serializers import JobSerializer
from .email_service import send_job_notification
from .permissions import IsAdminOrEmployer

User = get_user_model()


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    authentication_classes = [JWTAuthentication]

    # 🔐 Admin + Employer → create/update/delete
    # 👤 User → view only
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticated()]

    # 🔍 Admin & Employer → all jobs
    # 👤 User → only active jobs
    def get_queryset(self):
        user = self.request.user

        if (
            user.is_superuser or
            user.is_staff or
            getattr(user, "role", None) == "employer"
        ):
            return Job.objects.all()

        return Job.objects.filter(is_active=True)

    # 🧠 CREATE JOB
    def perform_create(self, serializer):
        job = serializer.save(created_by=self.request.user)

        if job.is_email_sent:
            return

        recipients = list(
            User.objects.filter(is_active=True)
            .exclude(email="")
            .values_list("email", flat=True)
        )

        next_path = f"/dashboard/apply/{job.id}"
        encoded_next = quote(next_path, safe="")
        email_link = f"{settings.FRONTEND_BASE_URL}/login?next={encoded_next}"

        subject = f"New Job Posted: {job.title}"

        message = (
            f"New Job Opportunity 🚀\n\n"
            f"Title: {job.title}\n"
            f"Location: {job.location}\n"
            f"Job Type: {job.job_type}\n"
            f"Experience: {job.experience}\n"
            f"Salary: {job.salary}\n\n"
            f"Click below to login & apply:\n"
            f"{email_link}"
        )

        if recipients:
            send_job_notification(subject, message, recipients)
            job.is_email_sent = True
            job.save(update_fields=["is_email_sent"])

    # ✅ SOFT DELETE (Admin + Employer)
    def destroy(self, request, *args, **kwargs):
        job = self.get_object()

        if not (
            request.user.is_superuser or
            request.user.is_staff or
            getattr(request.user, "role", None) == "employer"
        ):
            return Response(
                {"detail": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        job.is_active = False
        job.save(update_fields=["is_active"])

        return Response(
            {"detail": "Job deleted successfully"},
            status=status.HTTP_200_OK
        )
