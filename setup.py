# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schedulark',
 'schedulark.queue',
 'schedulark.queue.json',
 'schedulark.queue.memory',
 'schedulark.queue.sql',
 'schedulark.task',
 'schedulark.worker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'schedulark',
    'version': '0.1.6',
    'description': 'Job Scheduling Library',
    'long_description': None,
    'author': 'Knowark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

