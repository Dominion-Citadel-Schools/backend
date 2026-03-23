from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register
from about.models.vision import Vision


class VisionSeeder(BaseSeeder):

    dataset_file = "about/vision.yaml"

    def seed(self):

        data = self.load_dataset()

        vision_data = data["vision_section"]

        Vision.objects.update_or_create(
            section_type="vision",
            defaults={
                "headline": vision_data["headline"],
                "description": vision_data["description"],
                "academic_excellence": vision_data["academic_excellence"],
                "character_development": vision_data["character_development"],
                "global_citizenship": vision_data["global_citizenship"],
                "innovation": vision_data["innovation"],
                "is_active": vision_data["is_active"],
            }
        )

register(VisionSeeder)