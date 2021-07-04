from .connector import Connector, Connection


VERSION_KEY = 'SCHEDULARK_DBVERSION'
SETTINGS_TABLE = '__settings__'
TASKS_SCHEMA = 'public'
TASKS_TABLE = '__tasks__'


async def migrate(connector: Connector) -> None:
    try:
        connection = await connector.get()
        migrations = {key.replace('migration_', ''): value for key, value
                      in globals().items() if key.startswith('migration')}

        async with connection.transaction():
            current = await get_version(connection)
            for target, migration in migrations.items():
                await apply_migration(current, target, migration, connection)
    finally:
        await connector.put(connection)


async def apply_migration(current, target, migration, connection) -> None:
    if current >= target:  # pragma: no cover
        return None
    await migration(connection)
    table = f'{TASKS_SCHEMA}.{SETTINGS_TABLE}'
    await connection.execute(
        f'UPDATE {table} SET value = $1 WHERE key = $2', target, VERSION_KEY)


async def get_version(connection: Connection) -> str:
    table = f'{TASKS_SCHEMA}.{SETTINGS_TABLE}'
    await connection.execute(
        f'CREATE TABLE IF NOT EXISTS {table} (key TEXT, value TEXT)')
    result = await connection.fetch(
        f'SELECT key, value FROM {table} WHERE key = $1', VERSION_KEY)
    row = next(iter(result), {'value': '000'})
    return row['value']


async def migration_001(connection: Connection):
    table = f'{TASKS_SCHEMA}.{TASKS_TABLE}'
    await connection.execute(
        f'CREATE TABLE IF NOT EXISTS {table} ('
        'id UUID PRIMARY KEY, '
        'created_at TIMESTAMP, '
        'scheduled_at TIMESTAMP, '
        'picked_at TIMESTAMP, '
        'expired_at TIMESTAMP, '
        'job TEXT, '
        'attempts INTEGER, '
        'data JSONB, '
    ')')