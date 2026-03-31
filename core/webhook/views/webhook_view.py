from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from core.webhook.services.stats_service import StatsService


@csrf_exempt
@api_view(["POST"])
def sync_school_stats(request, version="v1"):
    try:
        #Simple token protection
        token = request.headers.get("X-API-KEY")

        if token != settings.SYNC_SECRET_KEY:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        StatsService.run_sync()

        return Response(
            {"message": "Stats synced successfully"},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )