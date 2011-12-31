from django.contrib.auth.models import User
from django.db import models
from slumlord.managers import TenantManager

class Tenant(models.Model):
    """
    Represents a tenant or client in a multi-tenant application.
    """
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(null=True)
    subdomain = models.SlugField(unique=True)
    custom_domain = models.URLField(unique=True, blank=True)

    objects = TenantManager()

    def __unicode__(self):
        return self.custom_domain or '{}.driftly.com'.format(self.subdomain)

    @property
    def slug(self):
        return "app_{}".format(self.pk)
