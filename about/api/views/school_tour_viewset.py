from django_filters.rest_framework import DjangoFilterBackend
from about.serializers.school_tour_serializer import SchoolTourSerializer
from about.api.services.school_tour_service import SchoolTourService
from core.mixins.audit_mixin import AuditViewSetMixin
from core.utils.viewsets import AdminWritePublicReadViewSet


class SchoolTourViewSet(AuditViewSetMixin,AdminWritePublicReadViewSet):
    serializer_class = SchoolTourSerializer
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

        return SchoolTourService.get_published_album_queryset(media_type)
