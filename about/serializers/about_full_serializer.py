from rest_framework import serializers
from about.serializers.histroy_nested_serilazer import HistoryNestedSerializer
from .vision_serializer import VisionSerializer
from .director_serializer import DirectorSerializer
from .school_tour_serializer import SchoolTourSerializer
from .song_serializer import SchoolSongSerializer


class AboutFullSerializer(serializers.Serializer):
    vision = VisionSerializer()
    mission = serializers.DictField()  # MissionSerializer() would be ideal, but we have pre-serialized data
    director = DirectorSerializer()
    school_tours = SchoolTourSerializer(many=True)
    school_song = SchoolSongSerializer()
    history =HistoryNestedSerializer()
 
    
  