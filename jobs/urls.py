from django.urls import path
from .views import pending_applications, invite_for_interview

urlpatterns = [
    path("admin/applications/pending/", pending_applications),
    path("admin/applications/invite/<int:app_id>/", invite_for_interview),
]
