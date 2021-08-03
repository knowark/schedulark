import os
import logging
from .schedulark import Schedulark
from .task import Task, Job
from .queue import Queue, MemoryQueue, SqlQueue


__version__ = '0.1.3'


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
