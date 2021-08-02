import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application


class Command(BaseCommand):
    """Management command for create Oauth2 application"""

    def handle(self, *args, **options):
        client_id = os.environ.get(
            'SOCIAL_AUTH_DRYCC_CONTROLLER_KEY') if os.environ.get(
            'SOCIAL_AUTH_DRYCC_CONTROLLER_KEY') else None
        client_secret = os.environ.get(
            'SOCIAL_AUTH_DRYCC_CONTROLLER_SECRET') if os.environ.get(
            'SOCIAL_AUTH_DRYCC_CONTROLLER_SECRET') else None
        controller_domain = os.environ.get('DRYCC_CONTROLLER_DOMAIN')
        if not all([client_id, client_secret, controller_domain]):
            self.stdout.write('client_id or client_secret non-existent')
            return
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write("Cannot create because there is no superuser")
        application, updated = Application.objects.update_or_create(
            name='Drycc Controller',
            defaults={
                'client_id': client_id,
                'client_secret': client_secret,
                'user': user,
                'redirect_uris': f'{controller_domain}/v2/complete/drycc/',
                'authorization_grant_type': 'authorization-code',
                'client_type': 'Public',
                'algorithm': 'RS256'
            }
        )
        if updated:
            self.stdout.write('Drycc controller app created')
        else:
            self.stdout.write("Drycc controller app updated")
