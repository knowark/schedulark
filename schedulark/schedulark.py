import asyncio
from datetime import datetime, timezone, timedelta
from typing import Type, Dict
from .job import Job, cronable
from .task import Task
from .queue import Queue, MemoryQueue
from .worker import Worker


class Schedulark:
    def __init__(self, queue=None) -> None:
        self.registry: Dict[str, Job] = {}
        self.queue = queue or MemoryQueue()
        self.worker = Worker(self.registry, self.queue)
        self.iterations = 0
        self.tick = 60

    def register(self, job: Job) -> None:
        self.registry[job.__class__.__name__] = job

    async def defer(self, job: str, data: Dict = None) -> None:
        task = Task(job=job, data=data)
        await self.queue.put(task)

    async def schedule(self) -> None:
        moment = datetime.now(timezone.utc)
        for job in self.registry.values():
            if not cronable(job.frequency, moment):
                continue
            task = Task(job=job.__class__.__name__)
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
