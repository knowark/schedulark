from typing import Dict
from ..task import Task


class Job:

    frequency = ''

    async def execute(self, task: Task) -> Dict:
        return {}
