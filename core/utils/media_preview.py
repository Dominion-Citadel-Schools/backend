from django.utils.html import format_html
import mimetypes


class MediaFieldResolver:
    """
    Responsible for extracting the media field from a model instance.
    """

    MEDIA_FIELD_CANDIDATES = ("file", "image", "audio", "video")

    @classmethod
    def resolve(cls, obj):
        for field_name in cls.MEDIA_FIELD_CANDIDATES:
            field = getattr(obj, field_name, None)
            if field and hasattr(field, "url"):
                return field
        return None


class MediaTypeResolver:
    """
    Responsible for determining media type.
    """

    @staticmethod
    def get_main_type(url: str) -> str | None:
        mime_type, _ = mimetypes.guess_type(url)
        if not mime_type:
            return None
        return mime_type.split("/")[0]


class MediaRenderer:
    """
    Responsible for rendering HTML for each media type.
    """

    @staticmethod
    def render_image(url, width, height):
        return format_html(
            '<img src="{}" width="{}" height="{}" style="object-fit:contain;" />',
            url,
            width,
            height,
        )

    @staticmethod
    def render_video(url, mime_type, width=None, height=None):
        style_parts = ["object-fit:contain;"]

        if width:
            style_parts.append(f"width:{width}px;")
        if height:
            style_parts.append(f"height:{height}px;")

        if not width and not height:
            style_parts.append("max-width:100%; height:auto;")

        style = " ".join(style_parts)

        return format_html(
        '<video controls style="{}">'
        '<source src="{}" type="{}">'
        'Your browser does not support the video tag.'
        '</video>',
        style,
        url,
        mime_type or "",
    )


    @staticmethod
    def render_audio(url, mime_type):
        return format_html(
            '<audio controls>'
            '<source src="{}" type="{}">'
            'Your browser does not support the audio element.'
            '</audio>',
            url,
            mime_type or "",
        )

    @staticmethod
    def render_file(url):
        return format_html('<a href="{}">Download file</a>', url)

# enforce 16:9 ratio for both image and video previews, with sensible defaults if dimensions are not available
def media_preview(obj, width=100, height=int(100 * 9 / 16)):
    """
    Public API function.
    Orchestrates resolution + detection + rendering.
    """

    media_field = MediaFieldResolver.resolve(obj)
    if not media_field:
        return "-"

    url = media_field.url
    mime_type, _ = mimetypes.guess_type(url)
    main_type = MediaTypeResolver.get_main_type(url)

    if main_type == "image":
        return MediaRenderer.render_image(url, width, height)

    if main_type == "video":
        return MediaRenderer.render_video(url, mime_type, width, height)

    if main_type == "audio":
        return MediaRenderer.render_audio(url, mime_type)

    return MediaRenderer.render_file(url)
