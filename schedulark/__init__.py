import os
import logging
from .planner import Planner
from .scheduler import Scheduler
from .task import Task, Job
from .queue import Queue, MemoryQueue, SqlQueue


__version__ = '0.1.5'


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
