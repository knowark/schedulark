from typing import Dict, Protocol
from ..base import Task


class Job(Protocol):
    name: str = ''
    lane: str = ''
    timeout: int = 300
    backoff: int = 3
    retries: int = 3
    frequency: str = '* * * * *'
    payload: dict = {}

    async def __call__(self, task: Task) -> Dict:
        """Job callback to be executed."""
