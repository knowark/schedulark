import os
import time
import json
import fcntl
from pathlib import Path
from typing import Dict, Optional
from contextlib import contextmanager
from ...base import Task
from ..queue import Queue


class JsonQueue(Queue):
    def __init__(self, path: str = '') -> None:
        self.path = path or 'tasks.json'
        self.time = time.time

    async def setup(self) -> None:
        path = Path(self.path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with locked_open(self.path, 'w') as f:
                f.write("{}")

    async def put(self, task: Task) -> None:
        if not os.path.exists(self.path):
            await self.setup()

        content: Dict = {}
        with locked_open(self.path, 'r+') as f:
            content.update(json.loads(f.read()))
            content[task.id] = vars(task)
            f.seek(f.truncate(0))
            f.write(json.dumps(content, indent=2))

    async def pick(self) -> Optional[Task]:
        if not os.path.exists(self.path):
            return None

        with locked_open(self.path, 'r+') as f:
            content: Dict = json.loads(f.read())

            now = self.time()
            tasks = [task for task in content.values()
                     if task['scheduled_at'] <= now and (
                         not task['picked_at'] or (
                             task['picked_at']
                             + task['timeout'] <= now))]

            if not tasks:
                return None

            tasks.sort(key=lambda task: task['scheduled_at'])
            task = tasks.pop(0)
            task['picked_at'] = int(time.time())
            content[task['id']] = task

            f.seek(f.truncate(0))
            f.write(json.dumps(content, indent=2))

            return Task(**task)

    async def remove(self, task: Task) -> None:
        if not os.path.exists(self.path):
            return

        with locked_open(self.path, 'r+') as f:
            content: Dict = json.loads(f.read())

            if task.id in content:
                del content[task.id]

            f.seek(f.truncate(0))
            f.write(json.dumps(content, indent=2))


@contextmanager
def locked_open(filename, mode='r'):
    with open(filename, mode) as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        yield file
        fcntl.flock(file, fcntl.LOCK_UN)
