import time
import logging
from typing import Dict
from .task import Task
from .queue import Queue, MemoryQueue


class Planner:
    def __init__(self, queue: Queue = None, timeout: int = 300) -> None:
        self.logger = logging.getLogger(__name__)
        self.queue = queue or MemoryQueue()
        self.timeout = timeout

    async def defer(self, job: str, data: Dict = None,
                    delay: int = 0, timeout: int = 0) -> None:
        self.logger.info(f'Deferring job <{job}>...')
        scheduled_at = int(time.time()) + delay
        expired_at = scheduled_at + (timeout or self.timeout)
        task = Task(job=job, scheduled_at=scheduled_at,
                    expired_at=expired_at, data=data)
        await self.queue.put(task)
