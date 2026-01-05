from .models import Application

def get_pending_interviews():
    return Application.objects.filter(status="pending")


def get_interview_candidates():
    return Application.objects.filter(status="interview")


def get_completed_interviews():
    return Application.objects.filter(status="completed")
