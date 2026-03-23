from rest_framework import viewsets
from ...models.program import Program
from ..serializers.program_serializer import ProgramSerializer
from django_filters.rest_framework import DjangoFilterBackend



class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides:
    - GET /programs/
    - GET /programs/{id}/
    """
    queryset = Program.objects.filter(is_active=True)
    serializer_class = ProgramSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]