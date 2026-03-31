from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from core.webhook.services.stats_service import StatsService
from core.webhook.models.school_dasboard_stat import SchoolStats


class Command(BaseCommand):
    help = "Sync school stats every 90 days"

    def handle(self, *args, **kwargs):
        last = SchoolStats.objects.first()

        if last and last.updated_at:
            if timezone.now() - last.updated_at < timedelta(days=90):
                self.stdout.write("Skipping (not yet 90 days)")
                return

        StatsService.run_sync()
        self.stdout.write(self.style.SUCCESS("Stats synced"))