from typing import Any, Generator
from fastapi.applications import FastAPI
import pytest
from fastapi.testclient import TestClient
from src.app import run_app


@pytest.fixture
def app_instance() -> Generator[FastAPI, Any, None]:
    yield run_app()

@pytest.fixture
def test_client(app_instance) -> Generator[TestClient, Any, None]:
    yield TestClient(app_instance)