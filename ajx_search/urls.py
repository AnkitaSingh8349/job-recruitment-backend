from django.urls import path
from .views import ai_job_search

urlpatterns = [
    path("ai-search/", ai_job_search),
]
