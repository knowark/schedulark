from pytest import mark
from schedulark.task import Task


pytestmark = mark.asyncio


def test_task_instantiation():
    task = Task()

    assert task is not None

    assert task.id is not None
    assert task.job == ''
    assert task.created_at > 0
    assert task.scheduled_at == 0
    assert task.picked_at is None
    assert task.expired_at is None
    assert task.attempts == 0
    assert task.data == {}


def test_task_attributes():
    data = {
        'tenant': 'knowark',
        'tid': '3cc2be35-b440-46e9-b67f-b294df945f97'
    }

    attributes = {
        'id': 'J001',
        'created_at': 1624895016,
        'scheduled_at': 1624898669,
        'data': data
    }

    task = Task(**attributes)

    assert task.id == attributes['id']
    assert task.created_at == attributes['created_at']
    assert task.scheduled_at == attributes['scheduled_at']
    assert task.picked_at is None
    assert task.attempts == 0
    assert task.data == data
