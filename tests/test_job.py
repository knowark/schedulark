from pytest import mark
from schedulark import Job


pytestmark = mark.asyncio


def test_job_instantiation():
    job = Job()

    assert job is not None

    assert job.id is not None
    assert job.name == 'Job'
    assert job.created_at > 0
    assert job.scheduled_at == 0
    assert job.reserved_at is None
    assert job.attempts == 0
    assert job.data == {}


def test_job_attributes():
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

    job = Job(**attributes)

    assert job.id == attributes['id']
    assert job.name == 'Job'
    assert job.created_at == attributes['created_at']
    assert job.scheduled_at == attributes['scheduled_at']
    assert job.reserved_at is None
    assert job.attempts == 0
    assert job.data == data


async def test_job_execute():
    job = Job()

    context = {'custom': 'execution data'}

    result = await job.execute(context)

    assert result == context


async def test_custom_job():
    class CustomJob(Job):
        async def execute(self, context: dict) -> dict:
            return {'data': 'updated'}

    job = CustomJob()

    data = {'data': 'new'}
    result = await job.execute(data)

    assert job.name == 'CustomJob'
    assert result == {'data': 'updated'}
