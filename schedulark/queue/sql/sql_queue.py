import time
import json
import asyncio
import threading
from json import dumps
from uuid import UUID
from datetime import datetime, timezone
from typing import Mapping, Dict, Optional
from ...base import Task
from ..queue import Queue
from .connector import Connector
from .migrations import (
    migrate, TASKS_SCHEMA, TASKS_TABLE)


class SqlQueue(Queue):
    def __init__(self, connector: Connector) -> None:
        self.connector = connector
        self.table = TASKS_TABLE
        self.schema = TASKS_SCHEMA

    async def setup(self):
        await migrate(self.connector)

    async def put(self, task: Task) -> None:
        query = """
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
        """

        connection = await self.connector.get()
        parameters = [
            task.id, datetime.fromtimestamp(task.created_at, timezone.utc),
            datetime.fromtimestamp(task.scheduled_at, timezone.utc),
            datetime.fromtimestamp(task.picked_at, timezone.utc),
            datetime.fromtimestamp(task.failed_at, timezone.utc),
            task.timeout, task.lane, task.job, task.attempts,
            dumps(task.payload)]

        await connection.fetch(query, *parameters)

    async def pick(self) -> Optional[Task]:
        query = f"""
        UPDATE public.__tasks__
        SET picked_at = NOW()::timestamptz
        WHERE id = (
            SELECT id FROM public.__tasks__
            WHERE scheduled_at <= NOW()::timestamptz
            AND (picked_at = 'epoch' OR (picked_at
            + interval '1 second' * timeout) <= NOW()::timestamptz)
            ORDER BY scheduled_at
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        )
        RETURNING *
        """

        connection = await self.connector.get()
        result = await connection.fetch(query)

        if not result:
            return None

        record = dict(result[0])
        record['id'] = str(record['id'])
        record['created_at'] = int(datetime.timestamp(
            record['created_at']))
        record['scheduled_at'] = int(datetime.timestamp(
            record['scheduled_at']))
        record['picked_at'] = int(datetime.timestamp(
            record['picked_at']))
        record['failed_at'] = int(datetime.timestamp(
            record['failed_at']))
        record['payload'] = json.loads(
            str(record['payload']))

        return Task(**record)

    async def remove(self, task: Task) -> None:
        query = f"""
        DELETE FROM public.__tasks__
        WHERE id = $1
        """

        connection = await self.connector.get()

        parameters = [task.id]

        await connection.fetch(query, *parameters)
