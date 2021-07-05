from typing import Dict, Protocol
from ..task import Task


class Job(Protocol):
    async def __call__(self, task: Task) -> Dict:
        """Job callback to be executed."""
