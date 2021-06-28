from typing import Type, Dict
from .job import Job


class Scheduler:
    def __init__(self) -> None:
        self.registry: Dict[str, Type[Job]] = {}

    def register(self, job_class: Type[Job]) -> None:
        self.registry[job_class.__name__] = job_class
