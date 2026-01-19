from django.db import models

# Create your models here.
# backend/userdashboard/models.py
from django.conf import settings
from django.db import models

class Interview(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interviews")
    role = models.CharField(max_length=200)
    # Use a single DateTime for date+time
    scheduled_at = models.DateTimeField()
    mode = models.CharField(max_length=100, blank=True)      # e.g., "Google Meet" / "Onsite"
    location = models.CharField(max_length=500, blank=True)  # e.g., meeting link or address
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_message = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_interviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-scheduled_at",)

    def __str__(self):
        return f"{self.role} -> {self.user} @ {self.scheduled_at}"
