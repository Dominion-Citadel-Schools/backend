from rest_framework import viewsets, status
from rest_framework.response import Response
from decouple import config
from academics.services.program_sync import update_program_capacity



# Example cURL command to test the webhook:
'''  url -X POST https://yourdomain.com/api/v1/academics/webhooks/enrollment-capacity/ 
    -H "Content-Type: application/json" 
    -H "X-Webhook-Secret: super-secret-key" 
    -d '{"id": 1, "enrollment_capacity": 120}'
'''


class ProgramCapacityWebhookViewSet(viewsets.ViewSet):
    """
    Webhook endpoint for updating program enrollment capacity.
    """

    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        secret = request.headers.get("X-Webhook-Secret")

        if secret != config("WEBHOOK_SECRET"):
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        program_id = request.data.get("id")
        capacity = request.data.get("capacity")

        if not program_id or capacity is None:
            return Response(
                {"error": "id and capacity are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        update_program_capacity(program_id, capacity)
    
        return Response({"status": "updated"}, status=status.HTTP_200_OK)
