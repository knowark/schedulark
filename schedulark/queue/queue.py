from typing import Optional
from abc import ABC, abstractmethod
from ..task import Task


class Queue(ABC):

    async def setup(self) -> None:
        """Optional setup procedures"""

    @abstractmethod
    async def put(self, task: Task) -> None:
        """Put method to be implemented"""

    @abstractmethod
    async def pick(self) -> Optional[Task]:
        """Retain method to be implemented"""

    @abstractmethod
    async def remove(self, task: Task) -> None:
        """Remove method to be implemented"""

    @abstractmethod
    async def size(self) -> int:
        """Size method to be implemented"""

    @abstractmethod
    async def clear(self) -> None:
        """Clear method to be implemented"""
