from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# ============================
# JOB MODEL
# ============================
class Job(models.Model):
    title = models.CharField(max_length=255, default="Not specified")
    company_name = models.CharField(max_length=255, default="Not specified")
    location = models.CharField(max_length=100, default="Not specified")
    job_type = models.CharField(max_length=50, default="Not specified")
    experience = models.CharField(max_length=50, default="Not specified")
    salary = models.CharField(max_length=50, default="Not specified")

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_email_sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)

# ============================
# APPLICATION MODEL
# ============================

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    phone = models.CharField(max_length=15, null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)

    expected_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    preferred_technology = models.CharField(max_length=100)
    cover_letter = models.TextField()

    status = models.CharField(max_length=50, default="Pending")
    admin_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
