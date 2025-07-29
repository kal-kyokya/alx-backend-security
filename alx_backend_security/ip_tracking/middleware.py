# ip_tracking/middleware.py
from django.http import HttpResponseForbidden # Import HttpResponseForbidden
from .models import RequestLog, BlockedIP # Import BlockedIP
import logging
from ipgeolocation import get_info as get_geolocation_info


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

        # --- Geolocation Logic (New for Task 2) ---
        country = None
        city = None
        if ip_address:
            try:
                # get_location_info handles caching internally for 24 hours by default
                geo_info = get_geolocation_info(ip_address)
                country = geo_info.get('country_name')
                city = geo_info.get('city')
                logger.debug(f"Geolocation for {ip_address}: Country={country}, City={city}")
            except Exception as err:
                # Handle cases where geolocation fails (e.g., local IP, invalid IP, service down)
                logger.error(f"Could not get geolocation for IP {ip_address}: {err}")
        # End Geolocation Logic

        # Log the request
        path = request.path
        method = request.method
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            RequestLog.objects.create(
                ip_address=ip_address,
                path=path,
                method=method,
                user_agent=user_agent,
                country=country,
                city=city
            )
            logger.info(f"Logged request: {ip_address} - {method} {path}")
        except Exception as e:
            logger.error(f"Error logging request {path} from {ip_address}: {e}")

        response = self.get_response(request)

        # Code to be executed for each request after the view is called.
        return response
