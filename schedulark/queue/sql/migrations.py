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
    await connection.execute(f"""
    INSERT INTO {table} (key, value)
        VALUES ($1, $2)
        ON CONFLICT (key)
        DO UPDATE SET value = EXCLUDED.value
    """, VERSION_KEY, target)


async def get_version(connection: Connection) -> str:
    table = f'{TASKS_SCHEMA}.{SETTINGS_TABLE}'
    await connection.execute(
        f'CREATE TABLE IF NOT EXISTS {table} (key TEXT UNIQUE, value TEXT)')
    result = await connection.fetch(
        f'SELECT key, value FROM {table} WHERE key = $1', VERSION_KEY)
    row = next(iter(result), {'value': '000'})
    return row['value']


async def migration_001(connection: Connection):
    table = f'{TASKS_SCHEMA}.{TASKS_TABLE}'
    await connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id UUID PRIMARY KEY,
        created_at TIMESTAMPTZ,
        scheduled_at TIMESTAMPTZ,
        picked_at TIMESTAMPTZ,
        expired_at TIMESTAMPTZ,
        job TEXT,
        status TEXT,
        attempts INTEGER,
        data JSONB)
    """)
