from uuid import uuid4
from time import time


class Task:
    def __init__(self, **attributes) -> None:
        self.id = str(attributes.get('id', str(uuid4())))
        self.created_at = int(attributes.get('created_at', time()))
        self.scheduled_at = int(attributes.get(
            'scheduled_at', self.created_at))
        self.picked_at = int(attributes.get('picked_at', 0))
        self.failed_at = int(attributes.get('failed_at', 0))
        self.timeout = int(attributes.get('timeout', 300))
        self.lane = attributes.get('lane', '')
        self.job = attributes.get('job', '')
        self.attempts = attributes.get('attempts', 0)
        self.payload = attributes.get('payload') or {}
