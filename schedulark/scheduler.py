import time
import asyncio
import logging
import inspect
from datetime import datetime, timezone, timedelta
from typing import Type, Tuple, Dict, Callable
from .task import Task, Job, cronable
from .queue import Queue, MemoryQueue
from .worker import Worker, Registry


class Scheduler:
    def __init__(self, queue: Queue = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.registry: Registry = {}
        self.queue = queue or MemoryQueue()
        self.worker = Worker(self.registry, self.queue)
        self.iterations = 0
        self.tick = 60

    def register(self, job: Job) -> None:
        name = getattr(job, 'name', getattr(
            job, '__name__', job.__class__.__name__))
        self.registry[name] = job

    async def setup(self) -> None:
        await self.queue.setup()

    async def work(self) -> None:
        await self.worker.start()

    async def time(self) -> None:
        self.iterations += 1
        while self.iterations:
            self.logger.info(f'Scheduling iteration #{self.iterations}...')
            now = datetime.now(timezone.utc)
            target = (now.replace(microsecond=0)
                      + timedelta(seconds=self.tick))
            delay = (target - now).total_seconds()
            await self.schedule()
            await asyncio.sleep(delay)
            self.iterations += 1

    async def schedule(self) -> None:
        moment = datetime.now(timezone.utc)
        for name, job in self.registry.items():
            frequency = getattr(job, 'frequency', '* * * * *')
            if not cronable(frequency, moment):
                continue

            data = getattr(job, 'data', None)
            timeout = getattr(job, 'timeout', 600)
            expired_at = int(datetime.timestamp(moment) + timeout)
            task = Task(job=name, expired_at=expired_at, data=data)
            await self.queue.put(task)
