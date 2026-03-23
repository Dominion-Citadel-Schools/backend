from academics.models.campuse import Campuse
from media_config.models.image import Image
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class CampuseSeeder(BaseSeeder):

    dataset_file = "academics/campuse.yaml"

    def seed(self):
        data = self.load_dataset()

        for item in data.get("Campuse", []):

            image = None
            if item.get("image"):
                image = Image.objects.filter(
                    file=item["image"]
                ).first()

            Campuse.objects.update_or_create(
                name=item["name"],
                defaults={
                    "location": item["location"],
                    "description": item["description"],
                    "year_established": item["year_established"],
                    "features": item.get("features", []),
                    "is_active": item.get("is_active", True),
                    "image": image,
                }
            )


register(CampuseSeeder)