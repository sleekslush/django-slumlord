from django.conf import settings
from django.db import DEFAULT_DB_ALIAS, connections, models

class PgSchemaHandler(object):
    default_search_path = ['"$user"', 'public']

    def __init__(self, using=None):
        """
        Constructs a new schema handler using the provided database.

        If no database was provided, it will use the one defined in 'MULTITENANT_DATABASE'
        setting. If that doesn't exist, it falls back to the default database
        in DATABASE_SETTINGS.
        """
        if not using:
            using = getattr(settings, 'MULTITENANT_DATABASE', DEFAULT_DB_ALIAS)

        self.connection = connections[using]

    def create_schema(self, name):
        """
        Creates a new schema with the provided name.
        """
        query = 'CREATE SCHEMA {}'.format(name)
        print query
        self._execute_query(query)

    def set_search_path(self, name, include_public=True):
        """
        Sets the search path to the schema specified in order to support queries
        in each Tenant's isolated namespace.

        If include_public is True, we also search the public schema. Otherwise,
        only the schema specified is searched.
        """
        search_path = [name] + (['public'] if include_public else [])
        self._set_schema_search_path(search_path)

    def reset_search_path(self):
        """
        Resets the search path to the default.
        """
        self._set_schema_search_path(self.default_search_path)

    def _set_schema_search_path(self, path):
        query = 'SET search_path TO {}'.format(','.join(path))
        self._execute_query(query)

    def _execute_query(self, query):
        self.connection.cursor().execute(query)
