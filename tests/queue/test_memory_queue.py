from pytest import mark
from schedulark.base import Task
from schedulark.queue import Queue, MemoryQueue


pytestmark = mark.asyncio


def test_memory_queue_instantiation():
    queue = MemoryQueue()

    assert isinstance(queue, Queue)


async def test_memory_queue_setup():
    queue = MemoryQueue()

    await queue.setup()

    assert queue._setup is True


async def test_memory_queue_put():
    queue = MemoryQueue()

    task_1 = Task(id='T001')
    task_2 = Task(id='T002')
    task_3 = Task(id='T003')

    await queue.put(task_1)
    await queue.put(task_2)
    await queue.put(task_3)

    assert task_1.id in queue.content
    assert task_2.id in queue.content
    assert task_3.id in queue.content


async def test_memory_queue_pick():
    queue = MemoryQueue()
    queue.time = lambda: 1_625_075_900
    queue.content = {
        'T001': Task(id='T001', scheduled_at=1_625_075_800),
        'T002': Task(id='T002', scheduled_at=1_625_075_400),
        'T003': Task(id='T003', scheduled_at=1_625_075_700)
    }

    task = await queue.pick()
    assert task.id == 'T002'

    task = await queue.pick()
    assert task.id == 'T003'

    task = await queue.pick()
    assert task.id == 'T001'

    task = await queue.pick()
    assert task is None


async def test_memory_queue_remove():
    task_1 = Task(id='T001')

    queue = MemoryQueue()
    queue.content = {
        'T001': task_1
    }

    await queue.remove(task_1)
    await queue.remove(task_1)

    assert queue.content == {}
