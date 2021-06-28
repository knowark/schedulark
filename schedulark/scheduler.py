import time
from typing import Type, Dict
from .job import Job


class Scheduler:
    def __init__(self, time=None) -> None:
        self.registry: Dict[str, Type[Job]] = {}
        self._time = time

    def time(self) -> int:
        return int(self._time and self._time() or time.time())

    def register(self, job_class: Type[Job]) -> None:
        self.registry[job_class.__name__] = job_class
