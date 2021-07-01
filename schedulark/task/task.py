from uuid import uuid4
from time import time


class Task:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', uuid4())
        self.created_at = attributes.get('created_at', int(time()))
        self.scheduled_at = attributes.get('scheduled_at', self.created_at)
        self.picked_at = attributes.get('picked_at', 0)
        self.expired_at = attributes.get('expired_at', 0)
        self.job = attributes.get('job', '')
        self.attempts = attributes.get('attempts', 0)
        self.data = attributes.get('data') or {}
