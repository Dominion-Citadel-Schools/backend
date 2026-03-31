from rest_framework import viewsets
from ...models.program import Program
from ..serializers.program_serializer import ProgramSerializer
#from django_filters.rest_framework import DjangoFilterBackend



class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns all active academic programs with campuses
    """

    serializer_class = ProgramSerializer

    def get_queryset(self):
        return (
            Program.objects
            .filter(is_active=True)
            .prefetch_related("campuses")
            .order_by("category", "id")
        )