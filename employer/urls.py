from django.urls import path
from .views import (
    EmployerRegisterView,
    EmployerProfileView,
    EmployerDashboardStatsView,  # ✅ ADD THIS
)

urlpatterns = [
    path("register/", EmployerRegisterView.as_view(), name="employer-register"),
    path("profile/", EmployerProfileView.as_view(), name="employer-profile"),
    path("dashboard/stats/", EmployerDashboardStatsView.as_view(), name="employer-dashboard-stats"),
]
