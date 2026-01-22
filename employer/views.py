from django.db.models import Q
from jobs.models import Application
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from userdashboard.models import Interview

from django.utils import timezone
from datetime import timedelta

from .serializers import EmployerRegisterSerializer
from jobs.models import Job
from .models import Employer


# =========================================
# EMPLOYER REGISTER
# =========================================
class EmployerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmployerRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "Employer registered successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "role": "employer"
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================
# EMPLOYER PROFILE (DASHBOARD DETAILS)
# =========================================
class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer = Employer.objects.get(user=request.user)

            return Response({
                "company_name": employer.company_name,
                "email": request.user.email,
            })

        except Employer.DoesNotExist:
            return Response(
                {"detail": "Employer profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# =========================================
# EMPLOYER DASHBOARD STATS (WITH EXPIRY DATE)
# =========================================
class EmployerDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        # ✅ Only logged-in employer jobs
        jobs = Job.objects.filter(created_by=request.user)

        # ✅ Total jobs
        total_jobs = jobs.count()

        # ✅ Active jobs (No expiry OR expiry in future)
        active_jobs = jobs.filter(
            Q(expiry_date__isnull=True) |
            Q(expiry_date__gte=now)
        ).count()

        # ✅ Expired jobs
        expired_jobs = jobs.filter(
            expiry_date__isnull=False,
            expiry_date__lt=now
        ).count()

        # ✅ Expiring soon (next 5 days)
        expiring_soon = jobs.filter(
            expiry_date__isnull=False,
            expiry_date__range=(now, now + timedelta(days=5))
        ).count()

        # ✅ Applications count
        applications = Application.objects.filter(
            job__created_by=request.user
        ).count()

        # ✅ Interviews count
        interviews = Interview.objects.filter(
            created_by=request.user
        ).count()

        # ✅ Hired candidates
        hired = Application.objects.filter(
            job__created_by=request.user,
            status="hired"
        ).count()

        return Response(
            {
                "total_jobs": total_jobs,
                "active_jobs": active_jobs,
                "expired_jobs": expired_jobs,
                "expiring_soon": expiring_soon,
                "applications": applications,
                "interviews": interviews,
                "hired": hired,
            },
            status=status.HTTP_200_OK
        )