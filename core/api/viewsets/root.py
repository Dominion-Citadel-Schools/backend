from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny






class ApiRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, version='v1'):

        base = request.build_absolute_uri()

        return Response({
            "service": "Dominion Schools API",
            "version": version,
            "core": {
                "homepage": f"{base}homepage/",
            },
            "academics": f"{base}academics/",
            "about": f"{base}about/",
            "contact": f"{base}contact/",
            "admissions": f"{base}admissions/",
            "testimonials": f"{base}testimonials/",
            "media" : f"{base}albums/",
            "webhooks": f"{base}webhook/sync-stats/",
        
        })



