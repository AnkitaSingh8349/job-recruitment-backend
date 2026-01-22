from .models import Application
from django.utils import timezone
from datetime import timedelta
from .models import Job
def get_pending_interviews():
    return Application.objects.filter(status="pending")


def get_interview_candidates():
    return Application.objects.filter(status="interview")


def get_completed_interviews():
    return Application.objects.filter(status="completed")
#================================================
#date ex
#==================================================

def get_employer_dashboard_stats(user):
    """
    Employer dashboard ke white cards ke liye stats
    """
    total_jobs = Job.objects.filter(created_by=user).count()

    active_jobs = Job.objects.filter(
        created_by=user,
        is_active=True
    ).count()

    expired_jobs = Job.objects.filter(
        created_by=user,
        is_active=False
    ).count()

    expiring_soon = Job.objects.filter(
        created_by=user,
        is_active=True,
        expiry_date__lte=timezone.now() + timedelta(days=5)
    ).count()

    return {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "expired_jobs": expired_jobs,
        "expiring_soon": expiring_soon,
    }
