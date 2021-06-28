from abc import ABC, abstractmethod
from .job import Job


class Queue(ABC):

    @abstractmethod
    def put(self, job: Job) -> None:
        """Put method to be implemented"""

    @abstractmethod
    def pop(self) -> Job:
        """Pop method to be implemented"""

    @abstractmethod
    def size(self) -> int:
        """Size method to be implemented"""

    @abstractmethod
    def clear(self) -> None:
        """Clear method to be implemented"""
