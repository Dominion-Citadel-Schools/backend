from django.core.cache import cache
from django.db.models import Count, Prefetch, Case, When
from gallery.models.album import GalleryAlbum
from gallery.models.media import GalleryMedia


class GalleryService:

    CACHE_TIMEOUT = 60 * 10  # 10 minutes

    @classmethod
    def get_published_album_queryset(cls, media_type=None):

        cache_key = f"published_album_ids:{media_type or 'all'}"

        album_ids = cache.get(cache_key)

        # STEP 1: Cache IDs
        if album_ids is None:
            base_qs = GalleryAlbum.objects.filter(is_published=True)

            if media_type:
                base_qs = base_qs.filter(album_type=media_type)

            album_ids = list(
                base_qs.order_by("-created_at")
                .values_list("id", flat=True)
            )

            cache.set(cache_key, album_ids, cls.CACHE_TIMEOUT)

        # STEP 2: Rebuild FULL queryset properly (IMPORTANT)
        queryset = GalleryAlbum.objects.filter(id__in=album_ids)

        # Preserve order
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(album_ids)]
        )

        queryset = queryset.order_by(preserved_order)

        # STEP 3: Reapply annotation
        queryset = queryset.annotate(
            media_count=Count("media_items", distinct=True)
        )

        # STEP 4: Reapply media filtering
        if media_type == "PICTURE":
            media_qs = GalleryMedia.objects.filter(image__isnull=False)
        elif media_type == "VIDEO":
            media_qs = GalleryMedia.objects.filter(video__isnull=False)
        else:
            media_qs = GalleryMedia.objects.all()

        queryset = queryset.prefetch_related(
            Prefetch(
                "media_items",
                queryset=media_qs,
                to_attr="filtered_media_items"  
            )
            
        )

        return queryset