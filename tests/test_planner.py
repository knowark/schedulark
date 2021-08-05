from pytest import mark
from typing import Dict
from schedulark import Planner, Job, Task


pytestmark = mark.asyncio


def test_planner_instantiation():
    planner = Planner()

    assert planner is not None


async def test_planner_setup():
    planner = Planner()
    await planner.setup()
    assert planner.queue._setup is True


async def test_planner_defer():
    class AlphaJob(Job):
        pass

    planner = Planner()
    queue = planner.queue

    data = {'hello': 'world'}
    await planner.defer('AlphaJob', data)

    task = await queue.pick()
    assert task.payload == data
