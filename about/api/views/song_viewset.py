from requests import Response
from models.song import SchoolSong
from serializers.song_serializer import SchoolSongSerializer
from about.api.services.school_songs_service import SchoolSongService
from core.utils.base_aboutsection_viewset import BaseAboutSectionViewSet


class SchoolSongViewSet(BaseAboutSectionViewSet):
    queryset = SchoolSong.objects.select_related("audio").all()
    serializer_class = SchoolSongSerializer

    def list(self, request, *args, **kwargs):
        ''' Returns active school song data '''
        data =SchoolSongService.get_queryset()
        return Response(data)