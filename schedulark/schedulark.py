import asyncio
from datetime import datetime, timezone, timedelta
from typing import Type, Tuple, Dict, Callable
from .task import Task, Job, cronable
from .queue import Queue, MemoryQueue
from .worker import Worker, Registry


class Schedulark:
    def __init__(self, queue=None) -> None:
        self.registry: Registry = {}
        self.queue = queue or MemoryQueue()
        self.worker = Worker(self.registry, self.queue)
        self.iterations = 0
        self.tick = 60

    def register(
        self, job: Callable, frequency: str = '', name: str = ''
    ) -> None:
        name = name or getattr(job, '__name__', job.__class__.__name__)
        self.registry[name] = (job, frequency)

    async def defer(self, job: str, data: Dict = None) -> None:
        task = Task(job=job, data=data)
        await self.queue.put(task)

    async def work(self) -> None:
        await self.worker.start()

    async def schedule(self) -> None:
        moment = datetime.now(timezone.utc)
        for job, (callback, frequency) in self.registry.items():
            if not cronable(frequency, moment):
                continue
            task = Task(job=job)
            await self.queue.put(task)

    async def time(self) -> None:
        self.iterations += 1
        while self.iterations:
            now = datetime.now(timezone.utc)
            target = (now.replace(microsecond=0)
                      + timedelta(seconds=self.tick))
            delay = (target - now).total_seconds()
            await asyncio.sleep(delay)
            await self.schedule()
            self.iterations += 1

    async def setup(self) -> None:
        await self.queue.setup()
