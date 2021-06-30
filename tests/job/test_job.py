from typing import Dict
from pytest import mark
from schedulark import Job
from schedulark.task import Task


pytestmark = mark.asyncio


def test_job_instantiation():
    job = Job()

    assert job.frequency == ''


async def test_job_execute():
    job = Job()

    result = await job.execute(Task())

    assert result == {}


async def test_custom_job():
    class CustomJob(Job):
        frequency = '*/5 * * * *'

        async def execute(self, task: Task) -> Dict:
            return {'data': 'updated'}

    job = CustomJob()

    data = {'data': 'new'}
    result = await job.execute(data)

    assert job.frequency == '*/5 * * * *'
    assert result == {'data': 'updated'}
