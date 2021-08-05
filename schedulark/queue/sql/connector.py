from typing import Protocol, List, Mapping, AsyncContextManager


class Connection(Protocol):
    async def fetch(self, query: str, *args, **kwargs) -> List[Mapping]:
        """Fetch the given query records"""


class Connector(Protocol):
    async def get(self, *args, **kwargs) -> Connection:
        """Get a connection from the pool"""
