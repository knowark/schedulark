from pytest import mark
from typing import Dict
from schedulark import Scheduler, Job, Task


pytestmark = mark.asyncio


def test_scheduler_instantiation():
    scheduler = Scheduler()

    assert scheduler is not None


def test_scheduler_register():
    class AlphaJob:
        async def __call__(self, task: Task) -> Dict:
            return {}

    class BetaJob:
        async def __call__(self, task: Task) -> Dict:
            return {}

    scheduler = Scheduler()

    scheduler.register(AlphaJob())
    scheduler.register(BetaJob())

    assert scheduler.registry['AlphaJob'].__class__ == AlphaJob
    assert scheduler.registry['BetaJob'].__class__ == BetaJob


async def test_scheduler_work():
    class MockWorker:
        async def start(self):
            self.started = True

    scheduler = Scheduler()
    scheduler.worker = MockWorker()

    await scheduler.work()

    assert scheduler.worker.started is True


async def test_scheduler_schedule():
    class AlphaJob:
        frequency = ''

        async def __call__(self, task: Task) -> Dict:
            return {}

    class BetaJob:
        async def __call__(self, task: Task) -> Dict:
            return {}

    scheduler = Scheduler()

    scheduler.register(AlphaJob())
    scheduler.register(BetaJob())

    assert len(scheduler.queue.content) == 0

    await scheduler.schedule()

    assert len(scheduler.queue.content) == 1
    task = next(iter(scheduler.queue.content.values()))
    assert task.job == 'BetaJob'


async def test_scheduler_time():
    async def alpha_job(task: Task) -> Dict:
        return {}

    async def beta_job(task: Task) -> Dict:
        return {}

    scheduler = Scheduler()

    alpha_job.frequency = '* * * * *'
    beta_job.frequency = ''

    scheduler.register(alpha_job)
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
    scheduler = Scheduler()
    await scheduler.setup()
    assert scheduler.queue._setup is True
