from rest_framework.routers import DefaultRouter
from academics.api.views.activity_viewset import ActivityCategoryViewSet, ActivityViewSet, CocurricularAlldataViewSet
from academics.api.views.calendar_viewset import AcademicYearViewSet, SchoolCalendarViewSet
#from academics.api.views.academics_viewset import AcademicsViewSet
from .views.campuse_viewset import CampuseViewSet
from .views.program_viewset import ProgramViewSet

# academics API router
def get_v1_academics_router():
    router = DefaultRouter()
    router.register(r"campuses", CampuseViewSet, basename="campus")
    router.register(r"programs", ProgramViewSet, basename="program")
    router.register("activity-categories", ActivityCategoryViewSet, basename="activity-categories")
    router.register("activities", ActivityViewSet, basename="activities")
    router.register("", CocurricularAlldataViewSet, basename="co-curricular")
    router.register("academic-years", AcademicYearViewSet)
    router.register("school-calendar", SchoolCalendarViewSet, basename="calendar")
    #router.register(r'alldata', AcademicsViewSet, basename='alldata')
    return router
