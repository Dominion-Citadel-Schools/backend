from rest_framework import serializers
from about.models.mission import Mission, CoreValue


class CoreValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoreValue
        fields = ["id", "title", "description"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title too short.")
        return value

    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Description too short.")
        return value


class MissionSerializer(serializers.ModelSerializer):
    core_values = CoreValueSerializer(many=True)

    class Meta:
        model = Mission
        fields = ["id", "statement", "is_active", "core_values", "updated_at"]

    def validate_statement(self, value):
        if len(value.strip()) < 30:
            raise serializers.ValidationError("Mission statement too short.")
        return value

    def validate(self, attrs):
        core_values = self.initial_data.get("core_values", [])

        if len(core_values) < 3:
            raise serializers.ValidationError({
                "core_values": "At least 3 core values required."
            })

        return attrs

    def create(self, validated_data):
        core_values_data = validated_data.pop("core_values")
        mission = Mission.objects.create(**validated_data)

        for value in core_values_data:
            CoreValue.objects.create(mission=mission, **value)

        return mission

    def update(self, instance, validated_data):
        core_values_data = validated_data.pop("core_values", None)

        instance.statement = validated_data.get("statement", instance.statement)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()

        if core_values_data:
            instance.core_values.all().delete()
            for value in core_values_data:
                CoreValue.objects.create(mission=instance, **value)

        return instance
