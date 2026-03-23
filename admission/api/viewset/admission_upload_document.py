from rest_framework.viewsets import ModelViewSet
from admission.api.serializers.serializer import AdmissionDocumentSerializer
from admission.models.admisssion_document import AdmissionDocument



class AdmissionDocumentViewSet(ModelViewSet):

    queryset = AdmissionDocument.objects.all()

    serializer_class = AdmissionDocumentSerializer