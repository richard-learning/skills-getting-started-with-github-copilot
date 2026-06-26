"""Pytest configuration and shared fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI application.
    
    The TestClient allows making HTTP requests to the FastAPI app
    without running a live server. Each test gets a fresh client instance.
    """
    return TestClient(app)
