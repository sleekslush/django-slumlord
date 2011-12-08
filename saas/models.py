from django.contrib.auth.models import User
from django.db import models
from saas.managers import TenantManager

class Tenant(models.Model):
    """
    Represents a tenant or client in a multi-tenant application.
    """
    owner = models.ForeignKey(User)
    subdomain = models.CharField(max_length=100, unique=True)
    custom_domain = models.URLField(unique=True, blank=True)

    objects = TenantManager()

    def get_app_schema(self):
        return 'app_{}'.format(self.id)

    def get_users_schema(self):
        return '{}_users'.format(self.get_app_schema())

    def get_full_schema(self):
        return '{}, {}'.format(self.get_app_schema(), self.get_users_schema())

    def __unicode__(self):
        return self.custom_domain or self.subdomain
