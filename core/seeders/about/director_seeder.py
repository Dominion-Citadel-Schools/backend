from about.models.director import DirectorMessage
from media_config.models.image import Image
from pathlib import Path
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class DirectorSeeder(BaseSeeder):

    dataset_file = "about/director_message.yaml"

    def seed(self):

        data = self.load_dataset()
        director_data = data["director_speech_section"]

        file_path = director_data.get("image")

        image = None

        if file_path:
            filename = Path(file_path).stem
            title = filename.replace("_", " ").title()

            image = Image.objects.filter(title=title).first()
        
            if not image:
                director_data.get("image")
                image = Image.objects.filter(
                    file=director_data["image"]
                ).first()
            
    
        DirectorMessage.objects.update_or_create(
            section_type="director_speech",
            defaults={
                "name": director_data["name"],
                "position": director_data["position"],
                "message": director_data["message"],
                "image": image,
                "is_active": director_data["is_active"],
            }
        )


register(DirectorSeeder)