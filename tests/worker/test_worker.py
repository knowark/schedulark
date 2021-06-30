from pytest import mark, fixture
from schedulark.job import Job
from schedulark.queue import MemoryQueue
from schedulark.task import Task
from schedulark.worker import Worker


pytestmark = mark.asyncio


class AlphaJob(Job):
    pass


class BetaJob(Job):
    pass


@fixture
def registry():
    return {
        'AlphaJob': AlphaJob,
        'BetaJob': BetaJob
    }


@fixture
def queue():
    queue = MemoryQueue()
    queue.content = {
        'T001': Task(id='T001', scheduled_at=1_625_075_800),
        'T002': Task(id='T002', scheduled_at=1_625_075_400),
        'T003': Task(id='T003', scheduled_at=1_625_075_700)
    }
    return queue


def test_worker_instantiation(registry, queue):
    worker = Worker(registry, queue)

    assert worker is not None


async def test_worker_start(registry, queue):
    class AlphaJob:
        pass

    worker = Worker(registry, queue)
