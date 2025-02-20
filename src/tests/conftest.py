import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from service import app

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-docker", action="store_true", default=False, help="run docker integration tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "docker: mark test as requiring docker containers")


def pytest_collection_modifyitems(config, items):
    
    skip_docker = pytest.mark.skip(reason="need --run-docker option to run")
    just_skip = pytest.mark.skip(reason="skipping")
    for item in items:
        if "docker" in item.keywords and not config.getoption("--run-docker"):
            item.add_marker(skip_docker)
        if "skip" in item.keywords:
            item.add_marker(just_skip) 

@pytest.fixture
def test_client():
    """Fixture to create a FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def mock_env():
    """Fixture to ensure environment is clean for each test."""
    with patch.dict(os.environ, {}, clear=True):
        yield
