from typing import Dict
from pytest import mark, fixture
from schedulark.queue import MemoryQueue
from schedulark.task import Task, Job
from schedulark.worker import Worker


pytestmark = mark.asyncio


class AlphaJob:
    async def __call__(self, task: Task) -> Dict:
        return {}


class BetaJob:
    async def __call__(self, task: Task) -> Dict:
        return {}


class FailingBetaJob:
    name = 'BetaJob'
    retries = 5

    def __init__(self, executed_tasks):
        self.executed_tasks = executed_tasks

    async def __call__(self, task: Task) -> Dict:
        self.executed_tasks.append(task)
        raise Exception('Something went wrong with the job!')


@fixture
def registry():
    return {
        'AlphaJob': AlphaJob(),
        'BetaJob': BetaJob()
    }


@fixture
def queue():
    queue = MemoryQueue()
    queue.content = {
        'T001': Task(
            id='T001', job='AlphaJob', scheduled_at=1_625_075_800),
        'T002': Task(
            id='T002', job='BetaJob', scheduled_at=1_625_075_400),
        'T003': Task(
            id='T003', job='AlphaJob', scheduled_at=1_625_075_700)
    }
    return queue


def test_worker_instantiation(registry, queue):
    worker = Worker(registry, queue)

    assert worker is not None


async def test_worker_start(registry, queue):
    executed_tasks = []

    class AlphaJob:
        async def __call__(self, task: Task) -> Dict:
            nonlocal executed_tasks
            executed_tasks.append(task)
            return {}

    registry['AlphaJob'] = AlphaJob()

    worker = Worker(registry, queue)
    worker.iterations = -5
    worker.sleep = 0.01
    worker.rest = 0.001

    await worker.start()

    assert len(executed_tasks) == 2
    assert executed_tasks[0].id == 'T003'
    assert executed_tasks[0].picked_at > 0
    assert executed_tasks[1].id == 'T001'
    assert executed_tasks[1].picked_at > 0


async def test_worker_stop(registry, queue):
    worker = Worker(registry, queue)
    worker.iterations = 5

    worker.stop()

    assert worker.iterations == 0


async def test_worker_retries_with_backoff(registry, queue):
    executed_tasks = []

    registry['BetaJob'] = FailingBetaJob(executed_tasks)

    worker = Worker(registry, queue)
    worker.iterations = -2
    worker.sleep = 0.01
    worker.rest = 0.001

    assert len(worker.queue.content) == 3
    assert worker.queue.content['T002'].attempts == 0
    assert worker.queue.content['T002'].failed_at == 0
    assert worker.queue.content['T002'].picked_at == 0
    assert worker.queue.content['T002'].scheduled_at == 1_625_075_400

    await worker.start()

    assert len(executed_tasks) == 1
    assert len(worker.queue.content) == 3
    assert worker.queue.content['T002'].attempts == 1
    assert worker.queue.content['T002'].failed_at > 0
    assert worker.queue.content['T002'].picked_at == 0
    assert worker.queue.content['T002'].scheduled_at == 1_625_075_403


async def test_worker_retries_with_exponential_backoff(registry, queue):
    executed_tasks = []

    registry['BetaJob'] = FailingBetaJob(executed_tasks)

    worker = Worker(registry, queue)
    worker.iterations = -6
    worker.sleep = 0.01
    worker.rest = 0.001

    await worker.start()

    assert worker.iterations == 0
    assert len(executed_tasks) == 5
    assert len(worker.queue.content) == 3
    assert worker.queue.content['T002'].attempts == 5
    assert worker.queue.content['T002'].failed_at > 0
    assert worker.queue.content['T002'].picked_at == 0
    assert worker.queue.content['T002'].scheduled_at == 1_625_075_493


async def test_worker_max_retries_reached(registry, queue):
    executed_tasks = []

    registry['BetaJob'] = FailingBetaJob(executed_tasks)

    worker = Worker(registry, queue)
    worker.iterations = -7
    worker.sleep = 0.01
    worker.rest = 0.001

    await worker.start()

    assert worker.iterations == 0
    assert len(executed_tasks) == 6
    assert len(worker.queue.content) == 2
    assert 'T002' not in worker.queue.content


async def test_worker_all_processed(registry, queue):
    executed_tasks = []

    registry['BetaJob'] = FailingBetaJob(executed_tasks)

    worker = Worker(registry, queue)
    worker.iterations = -8
    worker.sleep = 0.01
    worker.rest = 0.001

    await worker.start()

    assert worker.iterations == 0
    assert len(executed_tasks) == 6
    assert len(worker.queue.content) == 0
