from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError

from jobs.models import Application
from applications.serializers import (
    ApplicationSerializer,
    ApplicationCreateSerializer,
)
from .permissions import IsAdminOrEmployer


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # ✅ REQUIRED BY DRF (THIS FIXES THE ERROR)
    queryset = Application.objects.all()

    def get_queryset(self):
        # Swagger / Redoc fix
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()

        user = self.request.user
        qs = Application.objects.select_related("job")

        # ✅ ONLY SUPERUSER → all applications
        if user.is_superuser:
            return qs

        # ✅ Employer → only their jobs' applications
        if hasattr(user, "employer"):
            return qs.filter(job__created_by=user)

        # ✅ Candidate → their own applications
        return qs.filter(user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"detail": "Already applied"})

    # ==========================
    # ADMIN + EMPLOYER ACTIONS
    # ==========================

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrEmployer])
    def accept(self, request, pk=None):
        application = self.get_object()
        application.status = "Accepted"
        application.admin_message = request.data.get(
            "message", "Your application has been accepted."
        )
        application.save()

        return Response(
            {"message": "Application accepted successfully"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrEmployer])
    def reject(self, request, pk=None):
        application = self.get_object()
        application.status = "Rejected"
        application.admin_message = request.data.get(
            "message", "Your application has been rejected."
        )
        application.save()

        return Response(
            {"message": "Application rejected successfully"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrEmployer])
    def invite(self, request, pk=None):
        application = self.get_object()
        application.status = "Interview"
        application.admin_message = request.data.get(
            "message",
            "You are invited for an interview. We will contact you soon.",
        )
        application.save()

        return Response(
            {"message": "Interview invitation sent"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["delete"], permission_classes=[IsAdminOrEmployer])
    def remove(self, request, pk=None):
        application = self.get_object()
        application.delete()

        return Response(
            {"message": "Application deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
