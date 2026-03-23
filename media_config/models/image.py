from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from io import BytesIO
from media_config.models.base_media import BaseMedia


class Image(BaseMedia):

    IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
    MAX_SIZE = 5 * 1024 * 1024  # 5MB

    alt_text = models.CharField(max_length=150)

    file = models.FileField(
        upload_to="images/",
        validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)],
    )

    file_size = models.PositiveBigIntegerField(
    null=True,
    blank=True,
    db_index=True
)

    width = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    height = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    
    class Meta(BaseMedia.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["title"],
                name="unique_image_title"
            )
        ]

    def clean(self, *args, **kwargs):
        MAX_WIDTH = 1920
        MAX_HEIGHT = 1920
        QUALITY = 75 

        self.clean_title()

        if self.file and self.file.size > self.MAX_SIZE:
            raise ValidationError({"file": "Image too large (max 5MB)."})

        if not self.alt_text.strip():
            raise ValidationError({
                "alt_text": "Alt text is required for accessibility."
            })
        
        if not self.file:
          return
        
        try:
           img = PilImage.open(self.file)
           width, height = img.size

        except Exception:
            raise ValidationError("Invalid image file.")
        
        if height < 300:
         raise ValidationError("Image height must be at least 300px.")

        if width < 300:
         raise ValidationError("Image width must be at least 300px.")
        
        if self.file:
          img = PilImage.open(self.file)

          if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

            img.thumbnail(
            (MAX_WIDTH, MAX_HEIGHT)
        )

            width, height = img.size

            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=QUALITY)
            buffer.seek(0)

            self.file = ContentFile(
            buffer.read(),
            name=self.file.name
        )

            self.width = width
            self.height = height
            self.file_size = self.file.size

        
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)