import time
import json
from pathlib import Path
from typing import Dict, Optional
from ...base import Task
from ..queue import Queue


class JsonQueue(Queue):
    def __init__(self, path: str = '') -> None:
        self.path = path or 'tasks.json'
        self.time = time.time

    async def setup(self) -> None:
        path = Path(self.path)
        if not path.exists():
            path.write_text("{}")

    async def put(self, task: Task) -> None:
        path = Path(self.path)
        content: Dict = {}
        if path.exists():
            content.update(json.loads(path.read_text()))

        content[task.id] = vars(task)

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as f:
            json.dump(content, f, indent=2)

    async def pick(self) -> Optional[Task]:
        path = Path(self.path)
        if not path.exists():
            return None

        content: Dict = json.loads(path.read_text())

        now = self.time()
        tasks = [task for task in content.values()
                 if task['scheduled_at'] <= now and (
                     not task['picked_at'] or (
                         task['picked_at'] + task['timeout'] <= now))]

        if not tasks:
            return None

        tasks.sort(key=lambda task: task['scheduled_at'])
        task = tasks.pop(0)
        task['picked_at'] = int(time.time())
        content[task['id']] = task

        with path.open('w') as f:
            json.dump(content, f, indent=2)

        return Task(**task)

    async def remove(self, task: Task) -> None:
        path = Path(self.path)
        if not path.exists():
            return

        content: Dict = json.loads(path.read_text())

        if task.id in content:
            del content[task.id]

        with path.open('w') as f:
            json.dump(content, f, indent=2)
