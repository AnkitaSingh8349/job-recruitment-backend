from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("interview", "Interview Scheduled"),
        ("completed", "Interview Completed"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    interview_date = models.DateTimeField(null=True, blank=True)
    interview_link = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
from django.db import models

# Create your models here.
