from testimonials.models import Testimonial
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register
from django.utils import timezone


class TestimonialSeeder(BaseSeeder):

    dataset_file = "testimonials/testimonials.yaml"

    def seed(self):
        data = self.load_dataset()

        for item in data.get("Testimonial", []):

            obj, created = Testimonial.objects.update_or_create(
                full_name=item["full_name"],
                message=item["message"],
                defaults={
                    "role": item["role"],
                    "rating": item["rating"],
                    "graduation_year": item.get("graduation_year"),
                    "status": item.get("status", "PENDING"),
                    "is_active": item.get("is_active", True),
                }
            )

            # Handle moderation safely
            if obj.status in ["APPROVED", "REJECTED"] and not obj.moderated_at:
                obj.moderated_at = timezone.now()
                obj.save()
                

register(TestimonialSeeder)