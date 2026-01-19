from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "location")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "status",
        "admin_message",
        "created_at",   # ✅ FIXED
    )
    list_filter = ("status",)
    search_fields = ("user__username", "job__title")
