from pytest import mark
from schedulark.queue import Queue


pytestmark = mark.asyncio


def test_queue_methods():
    methods = Queue.__abstractmethods__  # type: ignore
    assert 'put' in methods
    assert 'pop' in methods
    assert 'size' in methods
    assert 'clear' in methods
