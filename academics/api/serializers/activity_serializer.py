from rest_framework import serializers
from academics.models.co_curriculum import Activity, ActivityCategory


class ActivityCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityCategory
        fields = "__all__"

    def validate_name(self, value):

        if len(value) < 3:
            raise serializers.ValidationError(
                "Category name must be at least 3 characters"
            )
        return value

    def validate(self, attrs):

        if attrs.get("order", 0) < 0:
            raise serializers.ValidationError(
                "Order cannot be negative"
            )
        return attrs


class ActivitySerializer(serializers.ModelSerializer):

    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Activity
        fields = "__all__"

    def validate_name(self, value):

        if len(value) < 2:
            raise serializers.ValidationError(
                "Activity name must contain at least 2 characters"
            )
        return value

    def validate(self, attrs):

        category = attrs.get("category")
        status = attrs.get("status")

        if category and status == "ACTIVE" and not category.is_active:
            raise serializers.ValidationError(
                "Cannot assign active activity to inactive category"
            )

        return attrs
    


class ActivityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = [
            "id",
            "name",
            "icon",
            "order",
        ]


class CoCurricularCategorySerializer(serializers.ModelSerializer):

    activities = ActivityListSerializer(many=True, read_only=True)

    class Meta:
        model = ActivityCategory
        fields = [
            "id",
            "name",
            "icon",
            "order",
            "activities",
        ]