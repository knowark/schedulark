from typing import List, Optional
from ..job import Job
from .queue import Queue


class MemoryQueue(Queue):
    def __init__(self) -> None:
        self.content: List[Job] = []

    async def put(self, job: Job) -> None:
        self.content.insert(0, job)

    async def pop(self) -> Optional[Job]:
        return self.content and self.content.pop() or None

    async def size(self) -> int:
        return len(self.content)

    async def clear(self) -> None:
        self.content.clear()
