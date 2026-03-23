from rest_framework.routers import DefaultRouter
from contact.api.viewsets.contact_viewsets import ContactMessageViewSet

contact_router = DefaultRouter()
contact_router.register(
    "",
    ContactMessageViewSet,
    basename="contact"
)