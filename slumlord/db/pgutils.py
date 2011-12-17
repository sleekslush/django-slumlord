from django.conf import settings
from django.db import DEFAULT_DB_ALIAS, connections, transaction

_schema_handler_cache = {}

def get_schema_handler(using=None):
    if using not in _schema_handler_cache:
        _schema_handler_cache[using] = PgSchemaHandler(using)

    return _schema_handler_cache[using]

def create_schema(schema, using=None):
    get_schema_handler(using).create_schema(schema)

def set_search_path(path, include_public=False, using=None):
    get_schema_handler(using).set_search_path(path, include_public)

class PgSchemaHandler(object):
    default_search_path = ['$user', 'public']

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
        self._execute_query('CREATE SCHEMA {}'.format(name))

    def set_search_path(self, path, include_public=False):
        """
        Sets the search path to the schema specified in order to support queries
        in each Tenant's isolated namespace.

        If include_public is True, we also search the public schema. Otherwise,
        only the schema specified is searched.
        """
        if isinstance(path, basestring):
            path = [path]

        if include_public:
            path = ['public'].extend(path)

        self._set_schema_search_path(path)

    def reset_search_path(self):
        """
        Resets the search path to the default.
        """
        self._set_schema_search_path(self.default_search_path)

    def _set_schema_search_path(self, path):
        format_placeholders = ','.join(['%s'] * len(path))
        query = 'SET search_path TO {}'.format(format_placeholders)
        self._execute_query(query, path)

    def _execute_query(self, query, params=None):
        try:
            self.connection.cursor().execute(query, params)
        finally:
            transaction.commit_unless_managed()
