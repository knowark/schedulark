from pytest import mark
from schedulark.queue import Queue


def test_queue_methods():
    methods = Queue.__abstractmethods__  # type: ignore
    assert 'put' in methods
    assert 'pick' in methods
    assert 'remove' in methods
    assert 'size' in methods
    assert 'clear' in methods
