from celery import shared_task
from django.utils.timezone import now, timedelta
from ip_tracking.models import SuspiciousIP
# Let's create the 'SuspiciousIP' model
