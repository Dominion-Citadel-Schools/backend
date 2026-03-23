from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from academics.models.co_curriculum import Activity, ActivityCategory
from academics.api.serializers.activity_serializer import (
    ActivitySerializer,
    ActivityCategorySerializer,
    CoCurricularCategorySerializer
)
from academics.services.activity_service import ActivityService





class ActivityCategoryViewSet(ModelViewSet):

    queryset = ActivityCategory.objects.all()
    serializer_class = ActivityCategorySerializer


class ActivityViewSet(ModelViewSet):

    queryset = Activity.objects.select_related("category").all()
    serializer_class = ActivitySerializer

    def perform_create(self, serializer):

        ActivityService.create_activity(serializer.validated_data)

    def perform_update(self, serializer):

        ActivityService.update_activity(
            self.get_object(),
            serializer.validated_data
        )

    def perform_destroy(self, instance):

        ActivityService.delete_activity(instance)



class CocurricularAlldataViewSet(ViewSet):

    @method_decorator(cache_page(60 * 30))
    @action(detail=False, methods=["get"], url_path="co-curricular")
    def co_curricular(self, request, version="v1"):

        categories = ActivityService.get_co_curricular_activities()

        serializer = CoCurricularCategorySerializer(categories, many=True)

        return Response(serializer.data)