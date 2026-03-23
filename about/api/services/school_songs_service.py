from about.models.song import SchoolSong
from about.utils.base_sections_service import BaseSectionService
from about.serializers.song_serializer import SchoolSongSerializer


class SchoolSongService(BaseSectionService):
    model = SchoolSong
    serializer_class = SchoolSongSerializer
    cache_key = "about:school_songs:active"
    select_related_fields = ("image",)
