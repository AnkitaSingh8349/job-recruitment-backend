from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import JobViewSet, EmployerJobListView

router = DefaultRouter()
router.register(r"jobs", JobViewSet, basename="job")

urlpatterns = [
    path("employer/jobs/", EmployerJobListView.as_view(), name="employer-jobs"),
]

urlpatterns += router.urls
