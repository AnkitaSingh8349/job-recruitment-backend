from django.db.models import Q, F
from .models import JobSearchIndex


def normalize_experience(exp):
    """
    '3+ Years' -> 3
    """
    if not exp:
        return None
    digits = "".join(filter(str.isdigit, exp))
    return int(digits) if digits else None


def normalize_salary(salary):
    """
    '₹3 LPA+' -> 300000
    """
    if not salary:
        return None
    digits = "".join(filter(str.isdigit, salary))
    return int(digits) * 100000 if digits else None


def ai_search_jobs(query, filters):
    """
    FINAL, FLEXIBLE, SAFE SEARCH
    """

    qs = JobSearchIndex.objects.filter(is_active=True)

    # 🧠 KEYWORD SEARCH (AJX, Python, Company, etc.)
    if query:
        words = query.lower().split()
        q_obj = Q()
        for word in words:
            q_obj |= (
                Q(title__icontains=word) |
                Q(company__icontains=word) |
                Q(keywords__icontains=word)
            )
        qs = qs.filter(q_obj)

    # 📍 LOCATION (flexible)
    location = filters.get("location")
    if location:
        qs = qs.filter(city__icontains=location)

    # 🕒 JOB TYPE (VERY IMPORTANT FIX)
    job_type = filters.get("job_type")
    if job_type:
        qs = qs.filter(job_type__icontains=job_type)

    # 🏠 WORK MODE (VERY IMPORTANT FIX)
    work_mode = filters.get("work_mode")
    if work_mode:
        qs = qs.filter(work_mode__icontains=work_mode)

    # 📈 EXPERIENCE (safe range)
    exp = normalize_experience(filters.get("experience"))
    if exp is not None:
        qs = qs.filter(
            experience_min__lte=exp,
            experience_max__gte=exp
        )

    # 💰 SALARY (minimum match)
    salary = normalize_salary(filters.get("salary"))
    if salary is not None:
        qs = qs.filter(salary_min__lte=salary)

    # ✅ RETURN SEARCH RESULT WITH job_id
    return qs.values("id").annotate(job_id=F("id"))
