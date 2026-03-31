from rest_framework import serializers
from academics.models.program import Program, ProgramCampus


class ProgramCampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramCampus
        fields = [
            "id",
            "campus_name",
            "features",
            "order",
        ]

    def validate_campus_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Campus name cannot be empty.")
        return value.strip()

    def validate_features(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Features must be a list.")

        for f in value:
            if not isinstance(f, str) or not f.strip():
                raise serializers.ValidationError(
                    "Each feature must be a non-empty string."
                )

        return [f.strip() for f in value]


class ProgramSerializer(serializers.ModelSerializer):
    campuses = ProgramCampusSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "category",
            "description",
            "enrollment_capacity",
            "full_day",
            "image_url",
            "campuses",
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value.strip()

    def validate_enrollment_capacity(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Enrollment must be greater than 0."
            )
        return value

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, "file"):
            request = self.context.get("request")
            url = obj.image.file.url
            return request.build_absolute_uri(url) if request else url
        return None