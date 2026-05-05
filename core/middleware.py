import time
from django.db import OperationalError, connection


class DatabaseRetryMiddleware:
    """
    Retries the request once when PostgreSQL is still starting up after a restart.
    This handles Railway's container restart race condition where Django connects
    while Postgres is in recovery mode.
    """

    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for attempt in range(self.MAX_RETRIES):
            try:
                return self.get_response(request)
            except OperationalError:
                if attempt == self.MAX_RETRIES - 1:
                    raise
                connection.close()
                time.sleep(self.RETRY_DELAY)
