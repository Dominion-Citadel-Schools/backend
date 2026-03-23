from media_config.models.image import Image
from PIL import Image as PILImage
from django.core.files.base import ContentFile
from io import BytesIO


class ImageService:

    
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1920
    QUALITY = 75  # compression quality (1–95)

    @staticmethod
    def create_image(**data):

        uploaded_file = data.get("file")

        if not uploaded_file:
            raise ValueError("Image file is required.")

        img = PILImage.open(uploaded_file)

        # Convert PNG with transparency properly
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize if too large (maintains aspect ratio)
        img.thumbnail(
            (ImageService.MAX_WIDTH, ImageService.MAX_HEIGHT)
        )

        width, height = img.size

        # Compress image
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=ImageService.QUALITY)
        buffer.seek(0)

        compressed_file = ContentFile(
            buffer.read(),
            name=uploaded_file.name
        )

        data["file"] = compressed_file
        data["width"] = width
        data["height"] = height
        data["file_size"] = compressed_file.size

        instance = Image.objects.create(**data)

        return instance
    
    
    @staticmethod
    def deactivate_image(image_id):
        image = Image.objects.get(id=image_id)
        image.is_active = False
        image.save()
        return image
