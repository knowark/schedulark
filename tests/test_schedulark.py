from pytest import mark
from schedulark import Schedulark, Job


pytestmark = mark.asyncio


def test_scheduler_instantiation():
    scheduler = Schedulark()

    assert scheduler is not None


def test_scheduler_register():
    class AlphaJob(Job):
        pass

    class BetaJob(Job):
        pass

    scheduler = Schedulark()

    scheduler.register(AlphaJob())
    scheduler.register(BetaJob())

    assert scheduler.registry['AlphaJob'].__class__ == AlphaJob
    assert scheduler.registry['BetaJob'].__class__ == BetaJob


async def test_scheduler_defer():
    class AlphaJob(Job):
        pass

    scheduler = Schedulark()
    scheduler.registry['AlphaJob'] = AlphaJob()
    queue = scheduler.queue

    data = {'hello': 'world'}
    await scheduler.defer('AlphaJob', data)

    task = await queue.pick()
    assert await queue.size() == 1
    assert task.data == data


async def test_scheduler_schedule():
    class AlphaJob(Job):
        frequency = '* * * * *'

    class BetaJob(Job):
        pass

    scheduler = Schedulark()
    scheduler.register(AlphaJob())
    scheduler.register(BetaJob())

    assert len(scheduler.queue.content) == 0

    await scheduler.schedule()

    assert len(scheduler.queue.content) == 1
    task = next(iter(scheduler.queue.content.values()))
    assert task.job == 'AlphaJob'
