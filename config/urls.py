from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.api.viewsets.root import ApiRootView
from django.contrib import admin
from django.contrib.auth.views import LogoutView



admin.site.site_header = "Dominion Citadel Schools Administration"
admin.site.site_title = "Dominion Schools CMS"
admin.site.index_title = "Welcome to Dominion Schools CMS"


urlpatterns = [
    path(
        "admin/logout/",
        LogoutView.as_view(
            template_name="registration/logged_out.html"
        ),
        name="admin_logout",
    ),
    path("admin/", admin.site.urls),
    path("api/<str:version>/",  ApiRootView.as_view(), name="api-root"),
    path("api/<str:version>/", include("core.api.urls")),
]

# work only on development 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)