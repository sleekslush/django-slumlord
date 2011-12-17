from django.db.models.signals import post_save
from django.dispatch import receiver
from slumlord.models import Tenant

@receiver(post_save, sender=Tenant, dispatch_uid='on-tenant-saved-schema-handler')
def on_tenant_saved(sender, instance, created, using, **kwargs):
    if not created:
        return

    # put it in the celery queue!
