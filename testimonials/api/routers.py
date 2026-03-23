from rest_framework.routers import DefaultRouter
from .viewsets.testimonial import TestimonialViewSet

router_testimonial = DefaultRouter()
router_testimonial.register("", TestimonialViewSet, basename="testimonials")

urlpatterns = router_testimonial.urls