import pytest

from tests.test_base import run_migrations


@pytest.fixture()
def migrations():
    run_migrations()
