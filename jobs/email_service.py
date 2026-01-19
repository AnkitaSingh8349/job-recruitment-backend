from django.core.mail import send_mail
from django.conf import settings

def send_job_notification(subject, message, recipients, html_message=None):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        html_message=html_message,
        fail_silently=False,
    ) 
