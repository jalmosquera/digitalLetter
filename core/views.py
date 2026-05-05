from django.http import JsonResponse
from django.db import connection


def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok", "database": "connected"})
    except Exception as e:
        return JsonResponse(
            {"status": "error", "database": "unavailable", "detail": str(e)},
            status=503,
        )
