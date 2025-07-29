# ip_tracking/middleware.py
from django.http import HttpResponseForbidden # Import HttpResponseForbidden
from .models import RequestLog, BlockedIP # Import BlockedIP
import logging


logger = logging.getLogger(__name__)


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view is called.
        
        # Get the client's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # --- IP Blacklisting Logic ---
        if ip_address and BlockedIP.objects.filter(ip_address=ip_address).exists():
            logger.warning(f"Blocked request from blacklisted IP: {ip_address} for path {request.path}")
            return HttpResponseForbidden("Access Denied: Your IP address has been blocked.")
        # --- End IP Blacklisting Logic ---

        # Log the request (from previous task)
        path = request.path
        method = request.method
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            RequestLog.objects.create(
                ip_address=ip_address,
                path=path,
                method=method,
                user_agent=user_agent
            )
            logger.info(f"Logged request: {ip_address} - {method} {path}")
        except Exception as e:
            logger.error(f"Error logging request {path} from {ip_address}: {e}")

        response = self.get_response(request)

        # Code to be executed for each request after the view is called.
        return response
