from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


# ============================
# JOB MODEL

class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    salary = models.CharField(max_length=50)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_email_sent = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    created_at = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # 👇 SYSTEM auto expiry set karega (30 days)
        if not self.expiry_date:
            self.expiry_date = self.created_at + timedelta(days=30)
        super().save(*args, **kwargs)

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
