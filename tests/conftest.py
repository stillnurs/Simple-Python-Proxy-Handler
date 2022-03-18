import pytest
import http.server
from src.server.proxy import Handler

@pytest.fixture(scope="class")
def handler():
    return Handler