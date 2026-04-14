from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from about.models.school_tour import SchoolTour
from about.models.school_tour_media import SchoolTourMedia


def clear_album_cache():
    cache.delete("published_album_ids:all")
    cache.delete("published_album_ids:PICTURE")
    cache.delete("published_album_ids:VIDEO")

@receiver(post_save, sender=SchoolTour)
def album_saved(sender, **kwargs):
    clear_album_cache()


@receiver(post_delete, sender=SchoolTour)
def album_deleted(sender, **kwargs):
    clear_album_cache()


@receiver(post_save, sender=SchoolTourMedia)
def media_saved(sender, **kwargs):
    clear_album_cache()

@receiver(post_delete, sender=SchoolTourMedia)
def media_deleted(sender, **kwargs):
    clear_album_cache()
