from pytest import mark
from schedulark.job import Job
from schedulark.queue import Queue, MemoryQueue


pytestmark = mark.asyncio


def test_memory_queue_instantiation():
    queue = MemoryQueue()

    assert isinstance(queue, Queue)


async def test_memory_queue_put():
    queue = MemoryQueue()

    job_1 = Job()
    job_2 = Job()
    job_3 = Job()

    await queue.put(job_1)
    await queue.put(job_2)
    await queue.put(job_3)

    assert queue.content == [job_3, job_2, job_1]


async def test_memory_queue_pop():
    queue = MemoryQueue()
    assert await queue.pop() is None

    job_1 = Job()
    job_2 = Job()
    job_3 = Job()

    queue.content = [job_3, job_2, job_1]

    job = await queue.pop()

    assert job is job_1
    assert queue.content == [job_3, job_2]


async def test_memory_queue_size():
    queue = MemoryQueue()

    job_1 = Job()
    job_2 = Job()
    job_3 = Job()

    queue.content = [job_3, job_2, job_1]

    assert await queue.size() == 3


async def test_memory_queue_clear():
    queue = MemoryQueue()

    job_1 = Job()
    job_2 = Job()
    job_3 = Job()

    queue.content = [job_3, job_2, job_1]

    await queue.clear()

    assert queue.content == []
