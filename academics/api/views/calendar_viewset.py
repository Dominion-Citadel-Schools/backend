from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from academics.models.acadmic_year import AcademicYear
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from academics.api.serializers.calendar_serializer import AcademicYearSerializer
from academics.services.calendar_service import CalendarService


class AcademicYearViewSet(ModelViewSet):

    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer


class SchoolCalendarViewSet(ViewSet):

    @method_decorator(cache_page(60 * 30))
    @action(detail=False, methods=["get"], url_path="current-calendar")
    def current_calendar(self, request, version="v1"):

        data = CalendarService.get_current_calendar()

        if not data:
            return Response(
                {"detail": "No active academic calendar found"},
                status=404
            )

        return Response(data)