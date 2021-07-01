import inspect
from pytest import fixture
from schedulark.queue.sql.connector import Connector, Connection


def test_connection_definition():
    functions = [item[0] for item in inspect.getmembers(
        Connection, predicate=inspect.isfunction)]
    assert 'execute' in functions
    assert 'fetch' in functions


def test_connector_definition():
    functions = [item[0] for item in inspect.getmembers(
        Connector, predicate=inspect.isfunction)]
    assert 'get' in functions
    assert 'put' in functions
