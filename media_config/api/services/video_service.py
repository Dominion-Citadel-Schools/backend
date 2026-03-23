from media_config.models.video import Video


class VideoService:

    @staticmethod
    def create_video(**data):
        video = Video.objects.create(**data)
        return video


    @staticmethod
    def deactivate_audio(audio_id):
        audio = Video.objects.get(id=audio_id)
        audio.is_active = False
        audio.save(update_fields=["is_active"])
        return audio