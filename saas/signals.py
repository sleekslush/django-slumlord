from django.db.models.signals import post_save
from django.dispatch import receiver
from saas.db.utils import PgSchemaHandler
from saas.models import Tenant

@receiver(post_save, sender=Tenant, dispatch_uid='on-tenant-saved-schema-handler')
def on_tenant_saved(sender, instance, created, using, **kwargs):
    if not created:
        return

    pg_schema_handler = PgSchemaHandler(using)
    pg_schema_handler.create_schema(instance.get_app_schema())
    pg_schema_handler.create_schema(instance.get_users_schema())
