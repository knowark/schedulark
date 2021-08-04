import asyncio
import logging
from typing import Type, Tuple, Dict, Callable
from ..task import Job
from ..queue import Queue


Registry = Dict[str, Job]


class Worker:
    def __init__(self, registry: Registry, queue: Queue) -> None:
        self.logger = logging.getLogger(__name__)
        self.registry = registry
        self.queue = queue
        self.iterations = 0
        self.sleep = 60
        self.rest = 1

    async def start(self) -> None:
        self.iterations += 1
        while self.iterations:
            self.logger.info(
                f'Work iteration #{self.iterations}...')
            task = await self.queue.pick()
            await self._process(task)
            self.iterations += 1

    def stop(self) -> None:
        self.iterations = 0

    async def _process(self, task) -> None:
        if not task:
            return await asyncio.sleep(self.sleep)

        job = self.registry[task.job]
        timeout = (task.expired_at - task.scheduled_at)
        await asyncio.wait_for(job(task), timeout=timeout)
        await self.queue.remove(task)
        await asyncio.sleep(self.rest)
