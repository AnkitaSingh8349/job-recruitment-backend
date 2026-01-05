from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "job",
        "status",
        "interview_date",
        "created_at",
    )

    list_filter = ("status", "job")
    search_fields = ("user__username", "job__title")

    actions = ["mark_interview", "mark_completed"]

    def mark_interview(self, request, queryset):
        queryset.update(status="interview")
    mark_interview.short_description = "Mark as Interview Scheduled"

    def mark_completed(self, request, queryset):
        queryset.update(status="completed")
    mark_completed.short_description = "Mark as Interview Completed"
