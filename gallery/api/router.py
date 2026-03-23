from rest_framework.routers import DefaultRouter
from gallery.views.album_viewset import GalleryAlbumViewSet




def get_media_type_routers():
    router = DefaultRouter()

    router.register(r"images", GalleryAlbumViewSet, basename="albums-images")
    router.register(r"videos", GalleryAlbumViewSet, basename="albums-videos")

    return router
