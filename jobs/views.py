from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.conf import settings
from urllib.parse import quote

from .models import Job
from .serializers import JobSerializer
from .email_service import send_job_notification

User = get_user_model()
class EmployerJobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.filter(created_by=request.user)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # 🔐 Permissions
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    # 🔍 Queryset + filters
    def get_queryset(self):
        user = self.request.user

        # 👑 Admin → all jobs
        if user.is_staff or user.is_superuser:
            queryset = Job.objects.all()

        # 🧑‍💼 Employer → only own jobs
        elif getattr(user, "role", None) == "employer":
            queryset = Job.objects.filter(created_by=user)

        # 👤 Candidate / others → only active jobs
        else:
            queryset = Job.objects.filter(is_active=True)

        # 🔍 Optional filters
        params = self.request.query_params
        title = params.get("title")
        company = params.get("company")
        location = params.get("location")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if company:
            queryset = queryset.filter(company_name__icontains=company)

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    # ✅ CREATE JOB
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
            f"Company: {job.company_name}\n"
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

    # 🗑️ Soft delete
    def destroy(self, request, *args, **kwargs):
        job = self.get_object()

        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        job.is_active = False
        job.save(update_fields=["is_active"])

        return Response(
            {"detail": "Job deleted successfully"},
            status=status.HTTP_200_OK,
        )
