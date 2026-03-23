
'''class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("IMAGE", "Image"),
        ("VIDEO", "Video"),
    ]

    IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
    VIDEO_EXTENSIONS = ["mp4", "mov", "avi"]

    title = models.CharField(max_length=120)
    file = models.FileField(
        upload_to="uploads/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=IMAGE_EXTENSIONS + VIDEO_EXTENSIONS
            )
        ]
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    alt_text = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def clean(self):
        self.title = self.title.strip()

        MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
        MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB

        if self.file:
          if self.media_type == "IMAGE" and self.file.size > MAX_IMAGE_SIZE:
           raise ValidationError({
            "file": "Image file too large (max 5MB)."
        })
          
        if self.media_type == "VIDEO" and self.file.size > MAX_VIDEO_SIZE:
          raise ValidationError({
            "file": "Video file too large (max 50MB)."
        })

        if not self.title:
            raise ValidationError({"title": "Title cannot be empty."})

        if not self.file:
            raise ValidationError({"file": "File is required."})

        extension = self.file.name.split(".")[-1].lower()

        if self.media_type == "IMAGE" and extension not in self.IMAGE_EXTENSIONS:
          raise ValidationError({
        "file": "File must be a valid image format."
    })

        if self.media_type == "VIDEO" and extension not in self.VIDEO_EXTENSIONS:
          raise ValidationError({
        "file": "File must be a valid video format."
    })

        if self.media_type == "IMAGE" and not self.alt_text.strip():
            raise ValidationError({
                "alt_text": "Alt text is required for accessibility on images."
            })
        

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
     self.full_clean()
     super().save(*args, **kwargs)
     '''