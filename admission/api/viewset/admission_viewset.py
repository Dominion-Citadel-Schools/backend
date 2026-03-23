from rest_framework.viewsets import ModelViewSet
from admission.models.admission_models import Admission
from admission.api.serializers.serializer import AdmissionSerializer
from ..services.admission_service import AdmissionService


class AdmissionViewSet(ModelViewSet):

    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

    def perform_create(self, serializer):

        AdmissionService.create_admission(serializer.validated_data)