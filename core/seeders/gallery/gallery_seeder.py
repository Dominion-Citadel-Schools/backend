from media_config.models.image import Image
from core.seeders.base_seeder import BaseSeeder
from core.seeders.registry import register
from gallery.models.album import GalleryAlbum
from gallery.models.media import GalleryMedia


class GallerySeeder(BaseSeeder):

    dataset_file = "gallery/gallery.yaml"

    def seed(self):

        data = self.load_dataset()["gallery_section"]["albums"]

        for album_data in data:

            cover = Image.objects.filter(
                file__icontains=album_data["cover_image"]
            ).first()

            album = GalleryAlbum.objects.update_or_create(
                title=album_data["title"],
                defaults={
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

                GalleryMedia.objects.create(
                    album=album,
                    image=image
                )
            album.is_published = album_data["is_published"]
            album.save()

register(GallerySeeder)