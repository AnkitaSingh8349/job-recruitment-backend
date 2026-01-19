from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from userdashboard.models import Interview   

from .serializers import EmployerRegisterSerializer
from jobs.models import Job  
from .models import Employer   # ✅ MISSING IMPORT FIXED


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
            #===============================
            #EmployerDashboardStatsView
            #================================

class EmployerDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer = Employer.objects.get(user=request.user)

            total_jobs = Job.objects.filter(employer=employer).count()
            applications = Application.objects.filter(
                job__employer=employer
            ).count()
            interviews = Interview.objects.filter(
                job__employer=employer
            ).count()
            hired = Application.objects.filter(
                job__employer=employer,
                status="hired"
            ).count()

            return Response({
                "total_jobs": total_jobs,
                "applications": applications,
                "interviews": interviews,
                "hired": hired
            }, status=status.HTTP_200_OK)

        except Employer.DoesNotExist:
            return Response(
                {"detail": "Employer not found"},
                status=status.HTTP_404_NOT_FOUND
            )
