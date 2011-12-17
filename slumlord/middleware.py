from slumlord.models import Tenant

class TenantMiddleware(object):
    def process_request(self, request):
        try:
            request.tenant = Tenant.objects.get_by_host(request.get_host())
        except Tenant.DoesNotExist:
            request.tenant = None
