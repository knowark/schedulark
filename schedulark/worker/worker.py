import time
import asyncio
import logging
from typing import Type, Tuple, Dict, Callable
from ..base import Job
from ..queue import Queue


Registry = Dict[str, Job]


class Worker:
    def __init__(self, registry: Registry, queue: Queue) -> None:
        self.logger = logging.getLogger(__name__)
        self.registry = registry
        self.queue = queue
        self.iterations = 0
        self.backoff = 3
        self.retries = 3
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
        retries = getattr(job, 'retries', self.retries)
        backoff = getattr(job, 'backoff', self.backoff)
        try:
            await asyncio.wait_for(job(task), timeout=task.timeout)
            await self.queue.remove(task)
        except Exception:
            self.logger.exception('{task.job}. Task processing failed.')
            task.scheduled_at += (backoff * (2 ** task.attempts))
            task.picked_at = 0
            task.failed_at = time.time()
            task.attempts += 1

            if task.attempts <= retries:
                await self.queue.put(task)
            else:
                await self.queue.remove(task)
                self.logger.info(f'{task.job}. Maximum number of retries '
                                 f'reached: {retries}. Task removed.')

        await asyncio.sleep(self.rest)
