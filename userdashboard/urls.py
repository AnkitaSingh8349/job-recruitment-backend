from django.urls import path
from .views import (
    user_dashboard,
    dashboard_jobs,
    dashboard_applications,

    # Interview APIs
    admin_create_interview,
    user_interviews,
    respond_interview,

    # Application actions (Admin)
    admin_accept_application,
    admin_reject_application,
)

urlpatterns = [
    # ============================
    # USER DASHBOARD
    # ============================
    path("", user_dashboard),
    path("jobs/", dashboard_jobs),
    path("applications/", dashboard_applications),

    # ============================
    # INTERVIEWS ✅ FINAL FIX
    # ============================
    path("interviews/", user_interviews),   # 🔥 user/ REMOVE kiya
    path("interview/respond/", respond_interview),

    # ============================
    # ADMIN ACTIONS
    # ============================
    path("admin/interview/create/", admin_create_interview),
    path("applications/<int:app_id>/accept/", admin_accept_application),
    path("applications/<int:app_id>/reject/", admin_reject_application),
]
