from uuid import uuid4
from time import time


class Job:
    def __init__(self, **attributes) -> None:
        self.name = self.__class__.__name__
        self.id = attributes.get('id', uuid4())
        self.created_at = attributes.get('created_at', int(time()))
        self.scheduled_at = attributes.get('scheduled_at', 0)
        self.reserved_at = attributes.get('reserved_at', None)
        self.attempts = attributes.get('attempts', 0)
        self.data = attributes.get('data', {})

    async def execute(self, context: dict) -> dict:
        return context
