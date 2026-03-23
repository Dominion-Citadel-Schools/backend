from gallery.api.serializers.album_serializer import GalleryAlbumSerializer
from gallery.api.services.gallery_service import GalleryService
from core.mixins.audit_mixin import AuditViewSetMixin
from core.utils.viewsets import AdminWritePublicReadViewSet
from django_filters.rest_framework import DjangoFilterBackend


class GalleryAlbumViewSet(AuditViewSetMixin, AdminWritePublicReadViewSet):

    serializer_class = GalleryAlbumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["album_type"]

    def get_queryset(self):
        path = self.request.path

        if "images" in path:
            media_type = "PICTURE"
        elif "videos" in path:
            media_type = "VIDEO"
        else:
            media_type = None

        return GalleryService.get_published_album_queryset(media_type)
    