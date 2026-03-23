from django.db import models


class AboutSectionUtilsModel(models.Model):

    SECTION_CHOICES = (
        ("history", "History"),
        ("vision", "Vision"),
        ("mission", "Mission"),
        ("director_speech", "Director Speech"),
        ("school_tour", "School Tour"),
        ("school_song", "School Song"),
    )

    section_type = models.CharField(
        max_length=50,
        choices=SECTION_CHOICES,
    )

    class Meta:
        abstract = True
