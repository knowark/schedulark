from typing import Dict
from ..job import Job
from ..queue import Queue


class Worker:
    def __init__(self, registry: Dict[str, Job], queue: Queue) -> None:
        self.registry = registry
        self.queue = queue

    async def start(self) -> None:
        """Start method to be implemented"""

    async def stop(self) -> None:
        """Stop method to be implemented"""
