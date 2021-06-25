# Schedulark

Job Scheduling Library

## Usage

The first thing you should do is to create an **Scheduler** instance

    from schedulark import Scheduler

    scheduler = Scheduler()

Then you should register **jobs** in the scheduler so that they can be
referenced and dispatched by your application. A **Job** is an object with
an **execute(context)** method which holds the information required by the
scheduler to enqueue and process it.

    from schedulark import Job


    class MaintenanceJob(Job):

        async def execute(self, context: dict) -> dict:
            n = context.get('n', 1000)
            a, b = 0, 1
            while a < n:
                a, b = b, a + b

            return {'data': a}
