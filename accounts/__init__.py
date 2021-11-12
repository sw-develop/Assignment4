from django.db.backends.signals import connection_created


def activate_db_optimize(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA synchronous = OFF;')
        cursor.execute('PRAGMA journal_mode = MEMORY;')
        cursor.execute('PRAGMA cache_size = 10000;')
        cursor.execute('PRAGMA temp_store = MEMORY;')
        

connection_created.connect(activate_db_optimize)