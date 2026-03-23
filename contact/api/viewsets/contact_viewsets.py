from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from contact.models import ContactMessage
from contact.api.serializer.contact_serializer import ContactMessageSerializer
from contact.api.services.contact_service import ContactService
from contact.utils.contactratethrottle import ContactRateThrottle


class ContactMessageViewSet(ModelViewSet):

    throttle_classes = [ContactRateThrottle]
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact = ContactService.create_contact(serializer.validated_data)

        return Response(
            ContactMessageSerializer(contact).data,
            status=status.HTTP_201_CREATED
        )