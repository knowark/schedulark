from typing import Dict, Protocol
from ..task import Task


class Job(Protocol):
    name: str = ''
    category: str = ''
    timeout: int = 300
    frequency: str = '* * * * *'
    payload: dict = {}

    async def __call__(self, task: Task) -> Dict:
        """Job callback to be executed."""
