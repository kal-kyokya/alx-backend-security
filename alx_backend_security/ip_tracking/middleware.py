from .models import RequestLog
import logging


logger = logging.getLogger(__name__)

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)

        response = self.get_response(request)

        return response

def process_request(self, request):
    """Logs the IP address, timestamp, and path of the incoming request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR')

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
    except Exception as err:
        logger.error(f"Error logging request {path} from {ip_address}: {err}")

