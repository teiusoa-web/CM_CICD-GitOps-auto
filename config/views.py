from django.db import connection
from django.db.utils import OperationalError
from django.http import JsonResponse


def health(request):
    """Kubernetes readiness/liveness target: GET /health/."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except OperationalError:
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)
    return JsonResponse({"status": "ok", "database": "ok"})
