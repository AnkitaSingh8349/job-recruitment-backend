from django.db.models.signals import post_save
from django.dispatch import receiver

from jobs.models import Job
from employer.models import Employer
from ajx_search.models import JobSearchIndex


@receiver(post_save, sender=Job)
def sync_job_search_index(sender, instance, **kwargs):
    """
    Job save hote hi JobSearchIndex me company name add/update karega
    """

    # ❌ Agar job inactive hai → index delete
    if not instance.is_active:
        JobSearchIndex.objects.filter(job_id=instance.id).delete()
        return

    # ✅ Employer se company name nikaalo
    employer = Employer.objects.filter(user=instance.created_by).first()
    company_name = employer.company_name if employer else ""

    # ✅ Index create / update
    JobSearchIndex.objects.update_or_create(
        job_id=instance.id,
        defaults={
            "title": instance.title,
            "company": company_name,          # ⭐ YAHI MAIN FIX HAI
            "keywords": instance.description or "",
            "city": instance.location,
            "job_type": instance.job_type,
            "work_mode": "onsite",
            "experience_min": 0,
            "experience_max": 10,
            "salary_min": 0,
            "salary_max": 0,
            "priority_score": 1.0,
            "is_active": True,
        }
    )
