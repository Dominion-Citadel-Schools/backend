from rest_framework import serializers
from about.serializers.mission_serializer import CoreValueSerializer, MissionSerializer



class MissionNestedSerializer(serializers.Serializer):
    mission = MissionSerializer(many=False, allow_null=False)
    corevalues = CoreValueSerializer(many=True, allow_null=False)
