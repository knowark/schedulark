from typing import Dict, Protocol
from ..task import Task


class Job(Protocol):
    name: str = ''
    timeout: int = 600
    frequency: str = '* * * * *'

    async def __call__(self, task: Task) -> Dict:
        """Job callback to be executed."""
