from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

from jobs.models import Job
from .serializers import JobSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def ai_job_search(request):
    try:
        query = request.data.get("query", "").strip()
        location = request.data.get("location")
        job_type = request.data.get("job_type")
        experience = request.data.get("experience")
        salary = request.data.get("salary")

        qs = Job.objects.filter(is_active=True)

        # 🔍 SEARCH: title OR company_name (multi-word)
        if query:
            words = query.split()
            q_obj = Q()
            for word in words:
                q_obj |= Q(title__icontains=word) | Q(company_name__icontains=word)
            qs = qs.filter(q_obj)

        # 📍 Location filter
        if location:
            qs = qs.filter(location__icontains=location)

        # 🕒 Job type filter (exact match)
        if job_type:
            qs = qs.filter(job_type=job_type)

        # 🎓 Experience filter
        if experience is not None and experience != "":
            qs = qs.filter(experience__gte=int(experience))

        # 💰 Salary filter
        if salary is not None and salary != "":
            qs = qs.filter(salary__gte=int(salary))

        serializer = JobSerializer(qs, many=True)

        return Response({
            "jobs_found": qs.exists(),
            "jobs": serializer.data
        })

    except Exception as e:
        return Response({
            "jobs_found": False,
            "jobs": [],
            "error": str(e)
        }, status=500)
