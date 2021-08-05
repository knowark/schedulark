import datetime
from datetime import timezone
from typing import List, Dict, Tuple, Mapping, Any
from json import dumps
from inspect import cleandoc
from uuid import UUID
from contextlib import AsyncExitStack
from pytest import mark, fixture
from schedulark.base import Task
from schedulark.queue import Queue, SqlQueue
from schedulark.queue.sql.connector import Connector, Connection


pytestmark = mark.asyncio


@fixture
def mock_connector():
    class MockConnection:
        def __init__(self) -> None:
            self.execute_query = ''
            self.execute_args: Tuple = ()
            self.execute_result = ''
            self.fetch_query = ''
            self.fetch_args: Tuple = ()
            self.fetch_result: List[Any] = []
            self.payload: Dict = {}

        async def execute(self, query: str, *args, **kwargs) -> str:
            self.execute_query = query
            self.execute_args = args
            return self.execute_result

        async def fetch(self, query: str, *args, **kwargs) -> List[Mapping]:
            self.fetch_query = query
            self.fetch_args = args
            return self.fetch_result

        def transaction(self):
            return AsyncExitStack()

        def load(self, payload) -> None:
            self.payload = payload

    class MockConnector:
        def __init__(self) -> None:
            self.connection = MockConnection()
            self.pool: List[Connection] = [self.connection]

        async def get(self, *args, **kwargs) -> Connection:
            return self.pool.pop()  # type: ignore

        async def put(self, connection: Connection, *args, **kwargs) -> None:
            self.pool.append(connection)

        def load(self, payload) -> None:
            self.connection.load(payload)

    return MockConnector()


async def test_sql_queue_instantiation(mock_connector):
    queue = SqlQueue(mock_connector)

    assert isinstance(queue, Queue)


async def test_sql_queue_put(mock_connector):
    queue = SqlQueue(mock_connector)
    connection = queue.connector.connection
    task = Task(
        id='b9d278d7-11f5-4817-ad12-69989a988457',
        created_at=1625160082,
        scheduled_at=1625160082,
        picked_at=0,
        lane='build',
        job='WebsiteCompilationJob',
        attempts=0,
        payload={
            'tenant': 'knowark',
            'tid': '7da5b9fc-7ca0-4156-8443-aa5caef5db1d'
        }
    )

    await queue.put(task)

    assert cleandoc(connection.fetch_query) == cleandoc(
        """
        INSERT INTO public.__tasks__ (
            id, created_at, scheduled_at, picked_at, failed_at,
            timeout, lane, job, attempts, payload
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
        ) ON CONFLICT (id) DO UPDATE SET (
            created_at, scheduled_at, picked_at, failed_at,
            timeout, lane, job, attempts, payload
        ) = (
            EXCLUDED.created_at, EXCLUDED.scheduled_at,
            EXCLUDED.picked_at, EXCLUDED.failed_at, EXCLUDED.timeout,
            EXCLUDED.lane, EXCLUDED.job, EXCLUDED.attempts,
            EXCLUDED.payload
        )
        RETURNING *
        """)

    assert connection.fetch_args == (
        'b9d278d7-11f5-4817-ad12-69989a988457',
        datetime.datetime(2021, 7, 1, 17, 21, 22, tzinfo=timezone.utc),
        datetime.datetime(2021, 7, 1, 17, 21, 22, tzinfo=timezone.utc),
        datetime.datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc),
        datetime.datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc),
        300,
        'build',
        'WebsiteCompilationJob',
        0,
        dumps({
            'tenant': 'knowark',
            'tid': '7da5b9fc-7ca0-4156-8443-aa5caef5db1d'
        })
    )


async def test_sql_queue_pick(mock_connector):
    queue = SqlQueue(mock_connector)
    connection = queue.connector.connection
    connection.fetch_result = [dict(
        id='b9d278d7-11f5-4817-ad12-69989a988457',
        created_at=datetime.datetime(
            2021, 7, 1, 17, 21, 22, tzinfo=timezone.utc),
        scheduled_at=datetime.datetime(
            2021, 7, 1, 17, 21, 22, tzinfo=timezone.utc),
        picked_at=datetime.datetime(
            1970, 1, 1, 0, 0, tzinfo=timezone.utc),
        failed_at=datetime.datetime(
            1970, 1, 1, 0, 0, tzinfo=timezone.utc),
        timeout=300,
        lane='build',
        job='WebsiteCompilationJob',
        attempts=0,
        payload='''{
            "tenant": "knowark",
            "tid": "7da5b9fc-7ca0-4156-8443-aa5caef5db1d"
        }'''
    )]

    result = await queue.pick()

    assert vars(result) == dict(
        id='b9d278d7-11f5-4817-ad12-69989a988457',
        created_at=1625160082,
        scheduled_at=1625160082,
        picked_at=0,
        failed_at=0,
        timeout=300,
        lane='build',
        job='WebsiteCompilationJob',
        attempts=0,
        payload={
            'tenant': 'knowark',
            'tid': '7da5b9fc-7ca0-4156-8443-aa5caef5db1d'
        }
    )


async def test_sql_queue_pick_empty(mock_connector):
    queue = SqlQueue(mock_connector)
    connection = queue.connector.connection

    result = await queue.pick()

    assert result is None
    assert cleandoc(connection.fetch_query) == cleandoc(
        """
        UPDATE public.__tasks__
        SET picked_at = NOW()::timestamptz
        WHERE id = (
            SELECT id FROM public.__tasks__
            WHERE (picked_at = 'epoch'
            AND scheduled_at <= NOW()::timestamptz)
            ORDER BY scheduled_at
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        )
        RETURNING *
        """)


async def test_sql_queue_remove(mock_connector):
    queue = SqlQueue(mock_connector)
    connection = queue.connector.connection
    task = Task(
        id='b9d278d7-11f5-4817-ad12-69989a988457'
    )

    result = await queue.remove(task)

    assert result is None
    assert cleandoc(connection.fetch_query) == cleandoc(
        """
        DELETE FROM public.__tasks__
        WHERE id = $1
        """)

    assert connection.fetch_args == (
        'b9d278d7-11f5-4817-ad12-69989a988457',
    )


async def test_sql_queue_setup(mock_connector):
    queue = SqlQueue(mock_connector)

    await queue.setup()
    connection = queue.connector.connection

    assert len(connection.fetch_query) > 0
