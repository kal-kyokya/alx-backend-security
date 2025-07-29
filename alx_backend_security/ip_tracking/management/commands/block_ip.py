#!/usr/bin/env python
"""
'block_ip' creates a Django custom management command.
"""
from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP


class Command(BaseCommand):
    help = 'Blocks a given IP address from accessing the application.'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block.')
        parser.add_argument('--reason', type=str, default='', help='Rationale behind blocking.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']

        try:
            blocked_ip, created = BlockedIP.objects.get_or_created(
                ip_address=ip_address,
                defaults={'reason': reason}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
            else:
                self.stdout.write(self.style.WARNING(f'IP: {ip_address} was already blocked.'))
                if reason and blocked_ip.reason != reason:
                    blocked_ip.reason = reason
                    blocked_ip.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated "reason" for IP: {ip_address}'))

        except Exception as err:
            raise CommandError(f'Error blocking IP {ip_address}: {err}')
