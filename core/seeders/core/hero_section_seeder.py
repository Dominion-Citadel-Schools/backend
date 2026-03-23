from core.models.herosection import HeroSection
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class HeroSectionSeeder(BaseSeeder):

    dataset_file = "core/hero_section.yaml"

    def seed(self):
        data = self.load_dataset()

        for item in data.get("HeroSection", []):

            HeroSection.objects.update_or_create(
                headline=item["headline"],
                defaults={
                    "subheadline": item["subheadline"],
                    "primary_cta_text": item["primary_cta_text"],
                    "primary_cta_url": item["primary_cta_url"],
                    "secondary_cta_text": item.get("secondary_cta_text", ""),
                    "secondary_cta_url": item.get("secondary_cta_url", ""),
                    "is_active": item.get("is_active", True),
                }
            )


register(HeroSectionSeeder)