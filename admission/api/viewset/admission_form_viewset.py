from rest_framework.viewsets import ReadOnlyModelViewSet
from admission.api.serializers.serializer import AdmissionFormSerializer
from admission.models.admission_form_builder import AdmissionForm



class AdmissionFormViewSet(ReadOnlyModelViewSet):

    queryset = AdmissionForm.objects.filter(is_active=True)

    serializer_class = AdmissionFormSerializer