from pytest import mark
from schedulark.base import Task


pytestmark = mark.asyncio


def test_task_instantiation():
    task = Task()

    assert task is not None

    assert task.id is not None
    assert task.job == ''
    assert task.lane == ''
    assert task.created_at > 0
    assert task.scheduled_at > 0
    assert task.picked_at == 0
    assert task.timeout == 300
    assert task.failed_at == 0
    assert task.attempts == 0
    assert task.payload == {}


def test_task_attributes():
    payload = {
        'meta': {
            'auth': {
                'tenant': 'knowark',
                'tid': '3cc2be35-b440-46e9-b67f-b294df945f97'
            }
        },
        'data': {
            'records': [{'001': {'Hello': 'World'}}]
        }
    }

    attributes = {
        'id': 'J001',
        'created_at': 1624895016,
        'scheduled_at': 1624898669,
        'lane': 'event',
        'payload': payload
    }

    task = Task(**attributes)

    assert task.id == attributes['id']
    assert task.created_at == attributes['created_at']
    assert task.scheduled_at == attributes['scheduled_at']
    assert task.picked_at == 0
    assert task.failed_at == 0
    assert task.attempts == 0
    assert task.payload == payload
