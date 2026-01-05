from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Application


@api_view(["GET"])
@permission_classes([IsAdminUser])
def pending_applications(request):
    applications = Application.objects.filter(status="pending")

    data = [
        {
            "id": app.id,
            "user": app.user.username,
            "job": app.job.title,
        }
        for app in applications
    ]

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def invite_for_interview(request, app_id):
    application = Application.objects.get(id=app_id)

    application.status = "interview"
    application.interview_date = request.data.get("interview_date")
    application.interview_link = request.data.get("interview_link")
    application.save()

    return Response({"message": "Interview invite sent"})
