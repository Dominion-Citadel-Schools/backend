from about.models.song import SchoolSong
from rest_framework import serializers
from media_config.api.serializers.audio_serializer import AudioSerializer



class SchoolSongSerializer(serializers.ModelSerializer):
    audio = AudioSerializer(read_only=True)

    class Meta:
        model = SchoolSong
        fields = "__all__"

    def validate_lyrics(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Lyrics too short.")
        return value
