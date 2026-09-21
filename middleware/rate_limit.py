import time
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings

class RateLimitMiddleware:
    """
    Blocks users if they send more than MAX_REQUESTS in WINDOW seconds.
    Uses cache to track request counts.
    """

    MAX_REQUESTS = 30
    WINDOW = 300 # 5 min

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            key = f"rate-limit:{request.user.id}"
        else:
            # fallback to IP if user not logged in
            ip = self.get_client_ip(request)
            key = f"rate-limit:{ip}"

        data = cache.get(key, {"count": 0, "start": time.time()})
        current_time = time.time()

        # reset window if expired
        if current_time - data["start"] > self.WINDOW:
            data = {"count": 0, "start": current_time}

        data["count"] += 1
        cache.set(key, data, timeout=self.WINDOW)

        if data["count"] > self.MAX_REQUESTS:
            return JsonResponse(
                {"error": "Rate limit exceeded. Try again later."}, status=429
            )

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip