from rest_framework import serializers
from academics.models.acadmic_year import AcademicYear, CalendarEvent


class CalendarEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalendarEvent
        fields = "__all__"

    def validate_title(self, value):

        if len(value) < 3:
            raise serializers.ValidationError(
                "Event title must be at least 3 characters"
            )

        return value


class AcademicYearSerializer(serializers.ModelSerializer):

    events = CalendarEventSerializer(many=True, read_only=True)

    class Meta:
        model = AcademicYear
        fields = "__all__"

    def validate(self, attrs):

        if attrs["start_date"] >= attrs["end_date"]:
            raise serializers.ValidationError(
                "Start date must be before end date."
            )

        return attrs