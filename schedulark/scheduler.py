import time as time_module
from typing import Type, Dict
from .job import Job
from .queue import Queue, MemoryQueue


class Scheduler:
    def __init__(self, time=None, queue=None) -> None:
        self.registry: Dict[str, Type[Job]] = {}
        self._time = time or time_module.time
        self._queue = queue or MemoryQueue()

    def time(self) -> int:
        return int(self._time())

    def register(self, job_class: Type[Job]) -> None:
        self.registry[job_class.__name__] = job_class
