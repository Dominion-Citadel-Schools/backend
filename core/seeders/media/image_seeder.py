from pathlib import Path
from media_config.models.image import Image
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class MediaSeeder(BaseSeeder):

    dataset_file = "media/images.yaml"

    def extract_title(self, file_path):

        filename = Path(file_path).stem

        return (
            filename
            .replace("_", " ")
            .replace("-", " ")
            .title()
        )

    def seed(self):

        data = self.load_dataset()

        for img in data["images"]:

            file_path = img["file"]

            title = self.extract_title(file_path)

            Image.objects.update_or_create(
                title=title,
                defaults={
                    "file": file_path,
                    "alt_text": title
                }
            )


register(MediaSeeder)