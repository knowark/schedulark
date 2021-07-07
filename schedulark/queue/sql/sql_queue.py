import time
import asyncio
import threading
from json import dumps
from uuid import UUID
from datetime import datetime
from typing import Mapping, Dict, Optional
from ...task import Task
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
        query = f"""
        INSERT INTO public.__tasks__ (
            id, created_at, scheduled_at, picked_at, expired_at,
            job, attempts, data
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8
        ) ON CONFLICT (id) DO UPDATE SET (
            created_at, scheduled_at, picked_at, expired_at,
            job, attempts, data
        ) = (
            EXCLUDED.created_at, EXCLUDED.scheduled_at,
            EXCLUDED.picked_at, EXCLUDED.expired_at,
            EXCLUDED.job, EXCLUDED.attempts, EXCLUDED.data
        )
        RETURNING *
        """

        connection = await self.connector.get()
        parameters = [
            task.id, datetime.fromtimestamp(task.created_at),
            datetime.fromtimestamp(task.scheduled_at),
            task.picked_at and datetime.fromtimestamp(
                task.picked_at) or None,
            task.expired_at and datetime.fromtimestamp(
                task.expired_at) or None,
            task.job, task.attempts, dumps(task.data)]

        await connection.fetch(query, *parameters)

    async def pick(self) -> Optional[Task]:
        query = f"""
        UPDATE public.__tasks__
        SET picked_at = NOW()::timestamp
        WHERE id = (
            SELECT id FROM public.__tasks__
            WHERE picked_at IS NULL
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
        record['picked_at'] = record['picked_at'] and int(
            datetime.timestamp(record['picked_at'])) or None
        record['expired_at'] = record['expired_at'] and int(
            datetime.timestamp(record['expired_at'])) or None

        return Task(**record)

    async def remove(self, task: Task) -> None:
        query = f"""
        DELETE FROM public.__tasks__
        WHERE id = $1
        """

        connection = await self.connector.get()

        parameters = [UUID(task.id)]

        await connection.fetch(query, *parameters)

    async def size(self) -> int:
        query = f"""
        SELECT COUNT(*) as count
        FROM public.__tasks__
        """

        connection = await self.connector.get()

        result = await connection.fetch(query)
        record: Mapping[str, int] = next(iter(result), {})

        return record.get('count', 0)

    async def clear(self) -> None:
        query = f"""
        DELETE FROM public.__tasks__
        """

        connection = await self.connector.get()

        await connection.fetch(query)
