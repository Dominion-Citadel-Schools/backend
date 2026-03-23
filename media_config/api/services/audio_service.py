from media_config.models.audio import Audio


class AudioService:

    @staticmethod
    def create_audio(**data):
        audio = Audio.objects.create(**data)

        # Hook for future: auto-calculate duration
        # audio.duration_seconds = extract_duration(audio.file)
        # audio.save(update_fields=["duration_seconds"])

        return audio
    
    @staticmethod
    def deactivate_audio(audio_id):
        audio = Audio.objects.get(id=audio_id)
        audio.is_active = False
        audio.save(update_fields=["is_active"])
        return audio
