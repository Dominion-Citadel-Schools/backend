from academics.models.program import Program
from media_config.models.image import Image
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class ProgramSeeder(BaseSeeder):

    dataset_file = "academics/program.yaml"

    def seed(self):
        data = self.load_dataset()

        for item in data.get("Program", []):

            image = None
            if item.get("image"):
                image = Image.objects.filter(
                    file=item["image"]
                ).first()

            Program.objects.update_or_create(
                title=item["title"],
                defaults={
                    "category": item["category"],
                    "grades": item["grades"],
                    "description": item["description"],
                    "key_features": item.get("key_features", []),
                    "full_day": item.get("full_day", True),
                    "is_active": item.get("is_active", True),
                    "image": image,
                }
            )


register(ProgramSeeder)