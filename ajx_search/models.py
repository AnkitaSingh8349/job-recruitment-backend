from django.db import models


class JobSearchIndex(models.Model):
    # Reference to Job table
    job_id = models.IntegerField(db_index=True)

    # Basic info
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)

    # Search keywords (AI + manual)
    keywords = models.TextField(
        help_text="comma separated keywords: react, django, remote, fresher"
    )

    # Location
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, default="India")

    # Job nature
    work_mode = models.CharField(
        max_length=20,
        choices=[
            ("remote", "Remote"),
            ("onsite", "Onsite"),
            ("hybrid", "Hybrid"),
        ],
    )

    job_type = models.CharField(
        max_length=30,
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("contract", "Contract"),
            ("internship", "Internship"),
        ],
    )

    # Experience
    experience_min = models.IntegerField(default=0)
    experience_max = models.IntegerField(default=0)

    # Salary
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)

    # Ranking / AI score
    priority_score = models.FloatField(default=0.0)

    # Status
    is_active = models.BooleanField(default=True)

    # Time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "job_search_index"
        indexes = [
            models.Index(fields=["job_id"]),
            models.Index(fields=["title"]),
            models.Index(fields=["company"]),
            models.Index(fields=["city"]),
            models.Index(fields=["work_mode"]),
            models.Index(fields=["job_type"]),
            models.Index(fields=["experience_min"]),
            models.Index(fields=["salary_min"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.company}"
