from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from testimonials.models import Testimonial
from django_filters.rest_framework import DjangoFilterBackend
from testimonials.api.serializers import TestimonialSerializer
from core.utils.viewsets import AdminWritePublicReadViewSet

class TestimonialViewSet(AdminWritePublicReadViewSet):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]
    CACHE_KEY = "approved_testimonials_list"


    def list(self, request, *args, **kwargs):

        if not request.user.is_staff:
            cached_data = cache.get(self.CACHE_KEY)

            if cached_data:
                return Response(cached_data)

            queryset = self.get_queryset().filter(status="approved")
            serializer = self.get_serializer(queryset, many=True)

            cache.set(self.CACHE_KEY, serializer.data, timeout=60 * 5)

            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
        

    @action(detail=True, methods=["patch"])
    def moderate(self, request, pk=None):
      testimonial = self.get_object()
      action_type = request.data.get("action")

      if action_type == "approve":
       testimonial.approve(request.user)

      elif action_type == "reject":
       testimonial.reject(request.user)

      else:
        return Response({"error": "Invalid action"}, status=400)
      
        cache.delete(self.CACHE_KEY)

      return Response({"status": testimonial.status})
