from rest_framework import viewsets
from ...models.campuse import Campuse
from ..serializers.campuse_serializer import CampuseSerializer



class CampuseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides:
    - GET /campuses/
    - GET /campuses/{id}/
    """
    serializer_class = CampuseSerializer

    def get_queryset(self):
        return Campuse.objects.filter(is_active=True)

