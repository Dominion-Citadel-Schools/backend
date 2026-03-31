# core/signals.py
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from .models.herosection import  HeroSection
from media_config.models.image import Image


HOMEPAGE_DEPENDENT_MODELS = [HeroSection, Image]

def invalidate_homepage_cache(sender, instance, **kwargs):
    cache.delete("homepage_data")


for model in HOMEPAGE_DEPENDENT_MODELS:
    post_save.connect(invalidate_homepage_cache, sender=model, dispatch_uid="homepage_cache_invalidator")
    post_delete.connect(invalidate_homepage_cache, sender=model, dispatch_uid="homepage_cache_invalidator")
