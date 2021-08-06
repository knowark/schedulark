import os
import logging
from .base import Task, Job
from .planner import Planner
from .scheduler import Scheduler
from .queue import Queue, MemoryQueue, SqlQueue, JsonQueue


__version__ = '0.1.7'


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
