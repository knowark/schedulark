from pytest import mark
from typing import Dict
from schedulark import Schedulark, Job, Task


pytestmark = mark.asyncio


def test_scheduler_instantiation():
    scheduler = Schedulark()

    assert scheduler is not None


def test_scheduler_register():
    class AlphaJob:
        async def __call__(self, task: Task) -> Dict:
            return {}

    class BetaJob:
        async def __call__(self, task: Task) -> Dict:
            return {}

    scheduler = Schedulark()

    scheduler.register(AlphaJob())
    scheduler.register(BetaJob())

    assert scheduler.registry['AlphaJob'][0].__class__ == AlphaJob
    assert scheduler.registry['BetaJob'][0].__class__ == BetaJob


async def test_scheduler_defer():
    class AlphaJob(Job):
        pass

    scheduler = Schedulark()
    scheduler.registry['AlphaJob'] = AlphaJob()
    queue = scheduler.queue

    data = {'hello': 'world'}
    await scheduler.defer('AlphaJob', data)

    task = await queue.pick()
    assert task.data == data


async def test_scheduler_work():
    class MockWorker:
        async def start(self):
            self.started = True

    scheduler = Schedulark()
    scheduler.worker = MockWorker()

    await scheduler.work()

    assert scheduler.worker.started is True


async def test_scheduler_schedule():
    class AlphaJob:
        async def __call__(self, task: Task) -> Dict:
            return {}

    class BetaJob:
        async def __call__(self, task: Task) -> Dict:
            return {}

    scheduler = Schedulark()

    frequency = '* * * * *'
    scheduler.register(AlphaJob(), frequency)
    scheduler.register(BetaJob())

    assert len(scheduler.queue.content) == 0

    await scheduler.schedule()

    assert len(scheduler.queue.content) == 1
    task = next(iter(scheduler.queue.content.values()))
    assert task.job == 'AlphaJob'


async def test_scheduler_time():
    async def alpha_job(task: Task) -> Dict:
        return {}

    async def beta_job(task: Task) -> Dict:
        return {}

    scheduler = Schedulark()

    frequency = '* * * * *'
    scheduler.register(alpha_job, frequency)
    scheduler.register(beta_job)
    scheduler.iterations = -3
    scheduler.tick = 0.01

    assert len(scheduler.queue.content) == 0

    await scheduler.time()

    assert len(scheduler.queue.content) == 2
    tasks = iter(scheduler.queue.content.values())
    assert next(tasks).job == 'alpha_job'
    assert next(tasks).job == 'alpha_job'


async def test_scheduler_setup():
    scheduler = Schedulark()
    await scheduler.setup()
    assert scheduler is not None
