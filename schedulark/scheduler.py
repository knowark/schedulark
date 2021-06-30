import time
from typing import Type, Dict
from .job import Job
from .task import Task
from .queue import Queue, MemoryQueue


class Scheduler:
    def __init__(self, queue=None, time_=None) -> None:
        self.registry: Dict[str, Job] = {}
        self.queue = queue or MemoryQueue()
        self._time = time_ or time.time

    def time(self) -> int:
        return int(self._time())

    def register(self, job: Job) -> None:
        self.registry[job.__class__.__name__] = job

    async def schedule(self, job: str, data: Dict = None) -> None:
        task = Task(job=job, data=data)
        await self.queue.put(task)
