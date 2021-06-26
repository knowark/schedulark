from schedulark import Scheduler


def test_scheduler_instantiation():
    scheduler = Scheduler()

    assert scheduler is not None
