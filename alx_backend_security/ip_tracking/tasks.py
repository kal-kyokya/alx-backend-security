from celery import shared_task
from django.utils.timezone import now, timedelta
from ip_tracking.models import RequestLog, SuspiciousIP


SENSITIVE_PATHS = ['/admin', '/login', '/reset-password']
TRESHOLD = 100

@shared_task
def detect_suspicious_ips():
    one_hour_ago = now() - timedelta(hours=1)

    # Get IPs with > 100 requests in the past hour
    heavy_traffic_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(req_count=models.Count('id'))
        .filter(req_count__gt=THRESHOLD)
    )

    for entry in heavy_traffic_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="High traffic: >100 requests/hour"
        )

    # Get IPs accessing sensitive paths
    sensitive_ips = (
        RequestLog.objects.filter(
            timestamp__gte=one_hour_ago,
            path__in=SENSITIVE_PATHS
        ).values_list('ip_address', flat=True).distinct()
    )

    for ip in sensitive_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="Accessed sensitive path"
        )
