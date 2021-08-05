import time
from typing import Dict, Optional
from ...base import Task
from ..queue import Queue


class MemoryQueue(Queue):
    def __init__(self) -> None:
        self.content: Dict[str, Task] = {}
        self.time = time.time

    async def setup(self) -> None:
        self._setup = True

    async def put(self, task: Task) -> None:
        self.content[task.id] = task

    async def pick(self) -> Optional[Task]:
        now = self.time()
        tasks = [task for task in self.content.values()
                 if not task.picked_at and task.scheduled_at <= now]

        if not tasks:
            return None

        tasks.sort(key=lambda task: task.scheduled_at)
        task = tasks.pop(0)
        task.picked_at = int(time.time())
        return task

    async def remove(self, task: Task) -> None:
        if task.id in self.content:
            del self.content[task.id]
