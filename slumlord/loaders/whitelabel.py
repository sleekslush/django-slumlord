"""
Wrapper for loading templates for whitelabel support
"""

from django.conf import settings
from django.template.loaders import filesystem
from django.utils._os import safe_join
from dzen.django import local_thread

class Loader(filesystem.Loader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Creates a specific loader path based on tenant id for whitelabeling
        """
        request = local_thread.current_request()
        whitelabel_dirs = settings.WHITELABEL_DIRS

        if request:
            for whitelabel_dir in whitelabel_dirs:
                try:
                    yield safe_join(whitelabel_dir, request.tenant.slug, template_name)
                except UnicodeDecodeError:
                    raise
                except ValueError:
                    pass

_loader = Loader()
