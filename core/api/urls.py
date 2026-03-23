from django.urls import path, include
from academics.api.routers import get_v1_academics_router, get_v1_webhook_router 
from .routers import get_v1_core_router
from about.api.router import about_full_view_router
from gallery.api.router import get_media_type_routers
from admission.api.routers import router_admission
from contact.api.router import contact_router
#from media_config.api.router import media_router
from testimonials.api.routers import router_testimonial
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Main API router get_v1_core_router()
urlpatterns = [
    # Core resources
    path("", include(get_v1_core_router().urls)),

    # about module
    path("about/", include(about_full_view_router.urls)),
    
    # Academics module
    path("academics/", include(get_v1_academics_router().urls)),

    # Admission module
    path("admissions/", include(router_admission.urls)),

    # Testimonials module
    path("testimonials/", include(router_testimonial.urls)),

    # Media module
    #path("media/", include(media_router.urls)),
    #path("gallery/", include(gallery_router.urls)),
    path("albums/", include(get_media_type_routers().urls)),

    # Contact module
    path("contact/", include(contact_router.urls)),

    # Webhooks
    path("webhooks/", include(get_v1_webhook_router().urls)),

    # Auth
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
