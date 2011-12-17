from django.db import models

class TenantManager(models.Manager):
    def get_by_host(self, host):
        """
        Get the tenant that is associated with the provided host.

        First try to get a tenant by domain, falling back to a lookup
        by subdomain.
        """
        try:
            return self.get_by_domain(host)
        except self.model.DoesNotExist:
            subdomain = self._get_subdomain(host)

            if not subdomain:
                raise self.model.DoesNotExist

            return self.get_by_subdomain(subdomain)

    def get_by_subdomain(self, subdomain):
        return self.get(subdomain=subdomain)

    def get_by_domain(self, domain):
        return self.get(custom_domain=domain)

    def _get_subdomain(self, host):
        parts = host.split('.')
        return '.'.join(parts[:-2]) if len(parts) > 2 else None
