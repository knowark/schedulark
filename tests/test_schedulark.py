from schedulark import Scheduler, Job


def test_scheduler_instantiation():
    scheduler = Scheduler()

    assert scheduler is not None


def test_scheduler_time():
    scheduler = Scheduler()

    assert scheduler.time() > 0

    def fake_time(): return 1624898475
    scheduler = Scheduler(time=fake_time)

    assert scheduler.time() == 1624898475


def test_scheduler_register():
    class AlphaJob(Job):
        pass

    class BetaJob(Job):
        pass

    scheduler = Scheduler()

    scheduler.register(AlphaJob)
    scheduler.register(BetaJob)

    assert scheduler.registry['AlphaJob'] == AlphaJob
    assert scheduler.registry['BetaJob'] == BetaJob
