from typing import Protocol, List, Mapping, AsyncContextManager


class Connection(Protocol):
    async def execute(self, query: str, *args, **kwargs) -> str:
        """Execute a query"""

    async def fetch(self, query: str, *args, **kwargs) -> List[Mapping]:
        """Fetch the given query records"""

    def transaction(self) -> AsyncContextManager:
        """Start a connection transaction"""


class Connector(Protocol):
    async def get(self, *args, **kwargs) -> Connection:
        """Get a connection from the pool"""

    async def put(self, connection: Connection, *args, **kwargs) -> None:
        """Return a connection to the pool"""
