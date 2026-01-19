from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status, serializers
from django.core.mail import send_mail
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from jobs.models import Job, Application
from jobs.serializers import JobSerializer
from applications.serializers import ApplicationSerializer

from .models import Interview
from .serializers import InterviewSerializer, CreateInterviewSerializer


# ==================================================
# Swagger serializer ONLY for documentation
# ==================================================
class InterviewResponseSwaggerSerializer(serializers.Serializer):
    interview_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=["accepted", "rejected"])
    message = serializers.CharField(required=False, allow_blank=True)


# ============================
# API: USER DASHBOARD OVERVIEW
# ============================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user = request.user
    return Response({
        "applied_count": Application.objects.filter(user=user).count(),
        "shortlisted_count": Application.objects.filter(user=user, status="shortlisted").count(),
        "rejected_count": Application.objects.filter(user=user, status="rejected").count(),
    })


# ============================
# API: USER DASHBOARD JOB LIST
# ============================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_jobs(request):
    jobs = Job.objects.filter(is_active=True).order_by("-created_at")
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


# ============================
# API: USER DASHBOARD APPLICATIONS
# ============================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_applications(request):
    applications = Application.objects.filter(user=request.user)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


# ==================================================
# ✅ ADMIN ACCEPT APPLICATION + EMAIL
# ==================================================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def admin_accept_application(request, app_id):
    try:
        app = Application.objects.get(id=app_id)
    except Application.DoesNotExist:
        return Response({"error": "Application not found"}, status=404)

    message = request.data.get("message", "")

    app.status = "accepted"
    app.admin_message = message
    app.save()

    send_mail(
        subject=f"Application Accepted – {app.job.title}",
        message=f"""
Hello {app.user.get_full_name() or app.user.username},

Your application for {app.job.title} has been ACCEPTED.

Message from HR:
{message}

Regards,
HR Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[app.user.email],
        fail_silently=False,
    )

    return Response({"message": "Application accepted & email sent"}, status=200)


# ==================================================
# ✅ ADMIN REJECT APPLICATION + EMAIL
# ==================================================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def admin_reject_application(request, app_id):
    try:
        app = Application.objects.get(id=app_id)
    except Application.DoesNotExist:
        return Response({"error": "Application not found"}, status=404)

    message = request.data.get("message", "")

    app.status = "rejected"
    app.admin_message = message
    app.save()

    send_mail(
        subject=f"Application Update – {app.job.title}",
        message=f"""
Hello {app.user.get_full_name() or app.user.username},

Thank you for applying for {app.job.title}.
Unfortunately, your application was not selected.

Message from HR:
{message}

Regards,
HR Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[app.user.email],
        fail_silently=False,
    )

    return Response({"message": "Application rejected & email sent"}, status=200)


# ===================================
# ADMIN CREATE INTERVIEW (DATE, TIME & LOCATION FROM POPUP)
# ===================================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def admin_create_interview(request):
    """
    Frontend must send:
    {
      user_id,
      role,
      scheduled_at,
      mode,
      location
    }
    """
    serializer = CreateInterviewSerializer(
        data=request.data,
        context={"request": request}
    )

    if serializer.is_valid():
        interview = serializer.save()
        send_interview_email_to_user(interview)
        return Response(
            {"message": "Interview created & email sent"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==============================================
# SEND INTERVIEW EMAIL TO USER
# ==============================================
def send_interview_email_to_user(interview):
    user = interview.user
    scheduled = interview.scheduled_at.strftime("%A, %d %B %Y at %I:%M %p")

    send_mail(
        subject=f"Interview Invitation – {interview.role}",
        message=f"""
Hello {user.get_full_name() or user.username},

You have been invited for an interview.

Role: {interview.role}
Date & Time: {scheduled}
Mode: {interview.mode}
Location: {interview.location}

Please login to your dashboard to Accept or Reject.

Regards,
HR Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


# =======================================
# USER SEES INTERVIEW ON DASHBOARD
# =======================================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_interviews(request):
    interviews = Interview.objects.filter(user=request.user)
    serializer = InterviewSerializer(interviews, many=True)
    return Response(serializer.data)


# ==================================================
# USER ACCEPT / REJECT INTERVIEW → ADMIN + USER EMAIL
# ==================================================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def respond_interview(request):
    interview_id = request.data.get("interview_id")
    status_val = request.data.get("status")
    message = request.data.get("message", "")

    if status_val not in ["accepted", "rejected"]:
        return Response({"error": "Invalid status"}, status=400)

    try:
        interview = Interview.objects.get(id=interview_id, user=request.user)
    except Interview.DoesNotExist:
        return Response({"error": "Interview not found"}, status=404)

    interview.status = status_val
    interview.admin_message = message
    interview.save()

    # EMAIL TO ADMIN
    send_mail(
        subject=f"Interview {status_val.upper()} – {interview.role}",
        message=f"""
Candidate: {request.user.email}
Role: {interview.role}
Status: {status_val}

Message:
{message}
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )

    # EMAIL TO USER
    send_mail(
        subject=f"Interview {status_val.capitalize()} – {interview.role}",
        message=f"""
Hello {request.user.get_full_name() or request.user.username},

Your interview response has been recorded.

Status: {status_val.upper()}

Regards,
HR Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

    return Response({"message": "Interview response processed"}, status=200)
