from pytest import mark
from schedulark import Scheduler, Job


pytestmark = mark.asyncio


def test_scheduler_instantiation():
    scheduler = Scheduler()

    assert scheduler is not None


def test_scheduler_time():
    scheduler = Scheduler()

    assert scheduler.time() > 0

    def fake_time(): return 1624898475
    scheduler = Scheduler(time_=fake_time)

    assert scheduler.time() == 1624898475


def test_scheduler_register():
    class AlphaJob(Job):
        pass

    class BetaJob(Job):
        pass

    scheduler = Scheduler()

    scheduler.register(AlphaJob())
    scheduler.register(BetaJob())

    assert scheduler.registry['AlphaJob'].__class__ == AlphaJob
    assert scheduler.registry['BetaJob'].__class__ == BetaJob


async def test_scheduler_defer():
    class AlphaJob(Job):
        pass

    scheduler = Scheduler()
    scheduler.registry['AlphaJob'] = AlphaJob()
    queue = scheduler.queue

    data = {'hello': 'world'}
    await scheduler.defer('AlphaJob', data)

    task = await queue.pick()
    assert await queue.size() == 1
    assert task.data == data
