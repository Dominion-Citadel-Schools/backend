from rest_framework.routers import DefaultRouter
from media_config.api.views.image_viewset import ImageViewSet
from media_config.api.views.video_viewset import VideoViewSet
from media_config.api.views.audio_viewset import AudioViewSet


media_router = DefaultRouter()
media_router.register("images", ImageViewSet)
media_router.register("videos", VideoViewSet)
media_router.register("audio", AudioViewSet)

urlpatterns = media_router.urls
