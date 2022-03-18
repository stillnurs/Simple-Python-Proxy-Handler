import pytest
from socket_server.proxy import Handler


@pytest.fixture(scope="class")
def handler():
    return Handler
