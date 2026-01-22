from django.core.management.base import BaseCommand
from jobs.utils import deactivate_expired_jobs


class Command(BaseCommand):
    help = "Deactivate expired jobs"

    def handle(self, *args, **kwargs):
        deactivate_expired_jobs()
        self.stdout.write(
            self.style.SUCCESS("Expired jobs deactivated successfully")
        )
