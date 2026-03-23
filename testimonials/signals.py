from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Testimonial


CACHE_KEY = "approved_testimonials_list"


@receiver(post_save, sender=Testimonial, dispatch_uid="invalidate_testimonial_cache_on_save")
def invalidate_testimonial_cache_on_save(sender, instance, **kwargs):
    cache.delete(CACHE_KEY)



@receiver(post_delete, sender=Testimonial, dispatch_uid="invalidate_testimonial_cache_on_delete")
def invalidate_testimonial_cache_on_delete(sender, instance, **kwargs):
    cache.delete(CACHE_KEY)

