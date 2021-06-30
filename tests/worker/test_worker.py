from pytest import mark, fixture
from schedulark.job import Job
from schedulark.queue import MemoryQueue
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
    return MemoryQueue()


def test_worker_instantiation(registry, queue):
    worker = Worker(registry, queue)

    assert worker is not None
