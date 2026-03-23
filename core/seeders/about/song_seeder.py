from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register
from about.models.song import SchoolSong
from media_config.models.audio import Audio


class SongSeeder(BaseSeeder):

    dataset_file = "about/school_song.yaml"

    def seed(self):

        data = self.load_dataset()

        song_data = data["school_song_section"]

        audio = None
        if song_data.get("audio"):
            audio = Audio.objects.filter(
                file=song_data["audio"]
            ).first()

        SchoolSong.objects.update_or_create(
            section_type="school_song",
            defaults={
                "title": song_data["title"],
                "lyrics": song_data["lyrics"],
                "audio": audio,
                "is_active": song_data["is_active"],
            }
        )

register(SongSeeder)