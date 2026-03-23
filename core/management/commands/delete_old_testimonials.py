from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from testimonials.models import Testimonial

class Command(BaseCommand):
    help = "Delete testimonials older than 30 days in trash"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=30)

        qs = Testimonial.objects.filter(
            is_deleted=True,
            deleted_at__lte=cutoff
        )

        count = qs.count()
        qs.delete()

        self.stdout.write(f"{count} testimonials permanently deleted.")