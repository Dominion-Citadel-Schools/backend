from pathlib import Path
from media_config.models.audio import Audio
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register


class AudioSeeder(BaseSeeder):

    dataset_file = "media/audios.yaml"

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

        for audio in data["audios"]:

            file_path = audio["file"]

            title = self.extract_title(file_path)

            Audio.objects.update_or_create(
                title=title,
                defaults={
                    "file": file_path
                }
            )


register(AudioSeeder)