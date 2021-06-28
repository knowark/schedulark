from typing import Optional
from abc import ABC, abstractmethod
from ..job import Job


class Queue(ABC):

    @abstractmethod
    async def put(self, job: Job) -> None:
        """Put method to be implemented"""

    @abstractmethod
    async def pop(self) -> Optional[Job]:
        """Pop method to be implemented"""

    @abstractmethod
    async def size(self) -> int:
        """Size method to be implemented"""

    @abstractmethod
    async def clear(self) -> None:
        """Clear method to be implemented"""
