# Schedulark

Job Scheduling Library

## Usage

First, you should define your **jobs** so that they can be registered,
referenced and dispatched by your application. A **Job** is an object with
an **execute(context)** method which holds the information required by the
scheduler to enqueue and process it.

```python
from schedulark import Job


class MaintenanceJob(Job):
    async def execute(self, context: dict) -> dict:
        number = context.get('number', 1000)
        first, second = 0, 1
        while first < number:
            first, second = second, fist + second

        return {'data': first}
```

Then you can create an **Scheduler** instance to control the arrangement and
processing of its registered jobs.

```python
from schedulark import Scheduler


scheduler = Scheduler()
scheduler.register(MaintenanceJob)
```


Finally, you might schedule (using cron expressions) one of the jobs you have
previously registered and so that it can be enqueued for execution.

```python
scheduler.schedule('MaintenanceJob', {'n': 777}, '0 0 * * *')
```

Summing up, the complete program using Schedulark would look like:

```python
import asyncio
from schedulark import Scheduler, Job


class MaintenanceJob(Job):
    async def execute(self, context: dict) -> dict:
        number = context.get('number', 1000)
        first, second = 0, 1
        while first < number:
            first, second = second, fist + second

        return {'data': first}


def main():
    scheduler = Scheduler()
    scheduler.register(MaintenanceJob)

    scheduler.schedule('MaintenanceJob', {'number': 765}, '0 0 * * *')
    scheduler.start()


if __name__ == '__main__':
    main()
    asyncio.get_event_loop().run_forever()
```
