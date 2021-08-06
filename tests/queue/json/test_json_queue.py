import json
from pytest import fixture, mark
from schedulark.base import Task
from schedulark.queue import Queue, JsonQueue


pytestmark = mark.asyncio


def test_json_queue_instantiation():
    queue = JsonQueue()

    assert isinstance(queue, Queue)


async def test_json_queue_setup(tmp_path):
    path = tmp_path / 'tasks.json'
    queue = JsonQueue(str(path))

    await queue.setup()
    assert path.exists()

    await queue.setup()
    assert path.read_text() == "{}"


async def test_json_queue_put(tmp_path):
    path = tmp_path / 'tasks.json'
    queue = JsonQueue(str(path))

    task_1 = Task(id='T001')
    task_2 = Task(id='T002')
    task_3 = Task(id='T003')

    await queue.put(task_1)
    await queue.put(task_2)
    await queue.put(task_3)

    content = json.loads(path.read_text())

    assert task_1.id in content
    assert task_2.id in content
    assert task_3.id in content


async def test_json_queue_pick(tmp_path):
    path = tmp_path / 'tasks.json'
    queue = JsonQueue(str(path))

    assert await queue.pick() is None

    queue.time = lambda: 1_625_075_900
    path.write_text(json.dumps({
        'T001': vars(Task(id='T001', scheduled_at=1_625_075_800)),
        'T002': vars(Task(id='T002', scheduled_at=1_625_075_400)),
        'T003': vars(Task(id='T003', scheduled_at=1_625_075_700))
    }))

    task = await queue.pick()
    assert task.id == 'T002'

    task = await queue.pick()
    assert task.id == 'T003'

    task = await queue.pick()
    assert task.id == 'T001'

    task = await queue.pick()
    assert task is None


async def test_memory_queue_remove(tmp_path):
    path = tmp_path / 'tasks.json'
    queue = JsonQueue(str(path))

    task_1 = Task(id='T001')

    await queue.remove(task_1)
    assert not path.exists()

    path.write_text(json.dumps({
        'T001': vars(task_1)
    }))

    await queue.remove(task_1)
    await queue.remove(task_1)

    assert path.read_text() == "{}"
