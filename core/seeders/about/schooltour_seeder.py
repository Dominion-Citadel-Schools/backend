from media_config.models.image import Image
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register
from about.models.school_tour import SchoolTour
from about.models.school_tour_media import SchoolTourMedia


class SchoolTourSeeder(BaseSeeder):

    dataset_file = "about/school_tour.yaml"

    def seed(self):

        data = self.load_dataset()["school_tour_section"]["albums"]

        for album_data in data:

            cover = Image.objects.filter(
                file__icontains=album_data["cover_image"]
            ).first()

            album = SchoolTour.objects.update_or_create(
                title=album_data["title"],
                defaults={
                "section_type": album_data["section_type"],
                "description": album_data["description"],
                "album_type": album_data["album_type"],
                "cover_image": cover,
                "event_date": album_data["event_date"],
                "is_published": False,
                }
            )[0]

            for media in album_data["media_items"]:

                image = None

                if media.get("image"):
                    image = Image.objects.filter(
                        file__icontains=media["image"]
                    ).first()

                    if not image:
                        raise Exception(f"Image not found: {media['image']}")

                if not image:
                    raise Exception(f"Invalid media entry: {media}")

                SchoolTourMedia.objects.create(
                    album=album,
                    image=image
                )
            album.is_published = album_data["is_published"]
            album.save()

register(SchoolTourSeeder)