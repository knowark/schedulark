from uuid import uuid4
from time import time


class Task:
    def __init__(self, **attributes) -> None:
        self.id = str(attributes.get('id', str(uuid4())))
        self.created_at = int(attributes.get('created_at', time()))
        self.scheduled_at = int(attributes.get(
            'scheduled_at', self.created_at))
        self.picked_at = int(attributes.get('picked_at', 0))
        self.expired_at = int(attributes.get(
            'expired_at', self.scheduled_at + 600))
        self.job = attributes.get('job', '')
        self.status = attributes.get('status', '')
        self.attempts = attributes.get('attempts', 0)
        self.data = attributes.get('data') or {}
