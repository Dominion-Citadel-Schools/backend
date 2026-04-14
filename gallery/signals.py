from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from gallery.models.album import GalleryAlbum
from gallery.models.media import GalleryMedia


def clear_album_cache():
    cache.delete("published_album_ids:all")
    cache.delete("published_album_ids:PICTURE")
    cache.delete("published_album_ids:VIDEO")

@receiver(post_save, sender=GalleryAlbum)
def album_saved(sender, **kwargs):
    clear_album_cache()


@receiver(post_delete, sender=GalleryAlbum)
def album_deleted(sender, **kwargs):
    clear_album_cache()


@receiver(post_save, sender=GalleryMedia)
def media_saved(sender, **kwargs):
    clear_album_cache()

@receiver(post_delete, sender=GalleryMedia)
def media_deleted(sender, **kwargs):
    clear_album_cache()

