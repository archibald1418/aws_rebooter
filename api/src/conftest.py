from typing import Any, Generator
import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def app_instance():
    yield app

@pytest.fixture
def test_client(app_instance) -> Generator[TestClient, Any, None]:
    yield TestClient(app)