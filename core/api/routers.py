from rest_framework.routers import DefaultRouter
from .viewsets import hompage


def get_v1_core_router():
    router = DefaultRouter()
    router.register(r"homepage", hompage.HomePageViewSet, basename="homepage")
    #router.register(r"media", media.MediaViewSet, basename="media")
    return router
