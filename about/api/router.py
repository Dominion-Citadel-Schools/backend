from rest_framework.routers import DefaultRouter
from about.api.views.school_tour_viewset import SchoolTourViewSet
from .views.about_full_view import AboutFullViewSet

about_full_view_router = DefaultRouter()
about_full_view_router.register("full", AboutFullViewSet, basename="about-full")
about_full_view_router.register("school-tour/images", SchoolTourViewSet, basename="school-tour-images")
about_full_view_router.register("school-tour/videos", SchoolTourViewSet, basename="school-tour-videos")



urlpatterns = about_full_view_router.urls
