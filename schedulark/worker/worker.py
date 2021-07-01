import asyncio
from typing import Dict
from ..job import Job
from ..queue import Queue


class Worker:
    def __init__(self, registry: Dict[str, Job], queue: Queue) -> None:
        self.registry = registry
        self.queue = queue
        self.iterations = 0
        self.sleep = 60
        self.rest = 1

    async def start(self) -> None:
        self.iterations += 1
        while self.iterations:
            task = await self.queue.pick()
            await self._process(task)
            self.iterations += 1

    def stop(self) -> None:
        self.iterations = 0

    async def _process(self, task) -> None:
        if not task:
            return await asyncio.sleep(self.sleep)

        job = self.registry[task.job]
        await job.execute(task)
        await asyncio.sleep(self.rest)
