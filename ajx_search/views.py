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

        qs = Job.objects.filter(is_active=True)

        # 🔍 MULTI-WORD SEARCH: "AJX java"
        if query:
            words = query.split()
            q_obj = Q()
            for word in words:
                q_obj &= (
                    Q(title__icontains=word) |
                    Q(company_name__icontains=word)
                )
            qs = qs.filter(q_obj)

        # 📍 Location
        if location:
            qs = qs.filter(location__icontains=location)

        # 🕒 Job type
        if job_type:
            qs = qs.filter(job_type__icontains=job_type)

        serializer = JobSerializer(qs, many=True)

        return Response({
            "jobs_found": qs.exists(),
            "jobs": serializer.data
        })

    except Exception as e:
        # 🔥 NEVER return HTML error to frontend
        return Response({
            "jobs_found": False,
            "error": str(e),
            "jobs": []
        }, status=500)
