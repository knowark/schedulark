from datetime import datetime
from pytest import raises
from schedulark.base import cronable


def test_cronable_every_minute():
    pattern = "* * * * *"
    moment = datetime(2020, 4, 21, minute=5)
    assert all(cronable(pattern, datetime(2020, 4, 21, minute=minute)) for
               minute in range(60))


def test_cronable_empty_pattern():
    pattern = ""
    moment = datetime(2020, 4, 21, minute=5)
    assert cronable(pattern, moment) is False


def test_cronable_every_5_minutes():
    pattern = "*/5 * * * *"
    moment = datetime(2020, 4, 21, minute=5)
    assert all(cronable(pattern, datetime(2020, 4, 21, minute=minute)) for
               minute in range(0, 60, 5))


def test_cronable_every_5_seconds():
    pattern = "*!5 * * * *"
    moment = datetime(2020, 4, 21, minute=5)
    assert all(cronable(pattern, datetime(2020, 4, 21, second=second)) for
               second in range(0, 60, 5))


def test_cronable_at_exactly_the_17_second():
    pattern = "!17 * * * *"
    moment = datetime(2020, 4, 21, minute=5)
    assert cronable(pattern, datetime(2020, 4, 21, second=17))
    assert not cronable(pattern, datetime(2020, 4, 21, second=34))
    assert not cronable(pattern, datetime(2020, 4, 21, second=51))


def test_cronable_every_6_hours():
    pattern = "* */6 * * *"
    moment = datetime(2020, 4, 21, minute=5)
    assert all(cronable(pattern, datetime(2020, 4, 21, hour=hour)) for
               hour in range(0, 24, 6))


def test_cronable_correct_date():
    assert cronable("* */6 21 * *", datetime(2020, 4, 21, hour=6))
    assert cronable("* * * * 1", datetime(2020, 4, 27))  # monday
    assert cronable("* * * * 7", datetime(2020, 5, 3))  # sunday
    assert cronable("* 12 * * 4", datetime(2020, 5, 7, hour=12))  # thu. noon
    assert cronable("10 8 * * *", datetime(2020, 1, 1, hour=8, minute=10))
    assert cronable("* * 15 * *", datetime(2020, 1, 15))
    assert cronable("*/30 */4 * 4 2", datetime(2020, 4, 28, hour=12))


def test_cronable_wrong_date():
    assert not cronable("* */6 21 * *", datetime(2020, 4, 21, hour=7))
    assert not cronable("* * * * 1", datetime(2020, 4, 30))
    assert not cronable("* * * * 7", datetime(2020, 5, 8))
    assert not cronable("* 12 * * 4", datetime(2020, 5, 7, hour=3))
    assert not cronable("10 8 * * *", datetime(2020, 1, 1, hour=5, minute=10))
    assert not cronable("* * 15 * *", datetime(2020, 1, 14))
    assert not cronable("*/30 */4 * 4 2", datetime(2020, 4, 28, hour=10))


def test_invalid_pattern():
    with raises(ValueError):
        cronable("* 8,9 * * *", datetime(2020, 5, 8))
    with raises(ValueError):
        cronable("* * * * 7-10", datetime(2020, 5, 8))
    with raises(ValueError):
        cronable("* * * * fri", datetime(2020, 5, 8))
