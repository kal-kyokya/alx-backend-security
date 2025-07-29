from django.db import models


class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField(
        null=True, blank=True,
        help_text="IP address of the client making the request."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the request was received."
    )
    path = models.CharField(
        max_length=255,
        help_text="The path of the requested URL."
    )
    method = models.CharField(
        max_length=10,
        help_text="HTTP method of the request (e.g., GET, POST)."
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        help_text="User-Agent header of the request"
    )
    country = models.CharField(
        max_length=56,
        help_text="Country from which the request is made"
    )
    city = models.CharField(
        max_length=168,
        help_text="The city from which the request is made"
    )

    class Meta:
        # Optional: Add ordering for easier Browse in admin/queries
        ordering = ['-timestamp']
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"{self.timestamp.isoformat()} - {self.ip_address} - {self.method} {self.path}"


class BlockedIP():
    ip_address = models.GenericIPAddressField(
        unique=True,
        help_text="IP address to block from accessing the application."
    )
    reason = models.TextField(
        blank=True,
        help_text="Optional reason for blocking this IP."
    )
    blocked_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this IP was blocked."
    )

    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"

    def __str__(self):
        return self.ip_address
