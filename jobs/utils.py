from django.utils import timezone
from .models import Job


def deactivate_expired_jobs():
    """
    Expired jobs ko automatically inactive kare
    """
    expired_jobs = Job.objects.filter(
        is_active=True,
        expiry_date__lt=timezone.now()
    )

    expired_jobs.update(is_active=False)
