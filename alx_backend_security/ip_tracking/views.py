from django.http import JsonResponse
from ratelimit.decorators import ratelimit # View the decorator
import logging


logger = logging.getLogger(__name__)

# --- Sensitive View: Example "Login" Endpoint ---
@ratelimit(key='ip', rate='10/m', block=True, method='POST') # Authenticated users (from IP)
@ratelimit(key='ip', rate='5/m', block=True, method='POST', group='anon') # Anonymous users (from IP)
def sensitive_login_attempt(request):
    """A dummy view representing a sensitive login endpoint, subject to rate limiting.
    - Authenticated users: 10 POST requests per minute per IP
    - Anonymous users: 5 POST requests per minute per IP.
    """

    if request.method == 'POST':
        # Simulate a login attempt
        username = request.POST.get('username')
        password = request.POST.get('password')

        logger.info(f"Login attempt received for user: {username} from IP: {request.META.get('REMOTEADDR')}")

        # In a real scenario, one would process login here
        # For this task, we just return a success/fail message
        if username == "test" and password == "password":
            return JsonResponse({"status": "Login successful"}, status=200)
        else:
            return JsonResponse({"status": "Invalid credentials"}, status=400)

    return JsonResponse({"Status": "Please use POST method for login"}, status=405)

# --- A general public view (optional, for comparison) ---
@ratelimit(key='ip', rate='30/m', block=False) # Example: 30 requests per minute, but don't block, just log.
def public_data_view(request):
    """A public view to demonstrate a different rate limit or no blocking.
    """
    logger.info(f"Access to public data from IP: {request.META.get('REMOTE_ADDR')}")
    return JsonResponse({"data": "This is public information. Access allowed."})
