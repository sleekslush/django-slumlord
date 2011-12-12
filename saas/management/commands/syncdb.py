try:
    from south.management.commands import syncdb
except ImportError:
    from django.core.management.commands import syncdb

from saas.db.utils import PgSchemaHandler

class Command(syncdb.Command):
    option_list = syncdb.Command.option_list

    def handle(self, *args, **options):
        if args:
            self._set_schema(args[0], options.get('database'))

        super(Command, self).handle_noargs(**options)

    def _set_schema(self, app_name, using):
        pg_schema_handler = PgSchemaHandler(using)
        pg_schema_handler.set_search_path(app_name, False)
