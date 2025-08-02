from fastapi.testclient import TestClient
import pytest
from schema.user import UserCreate
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_user_schema():
    return UserCreate(name='Gabriel', email='test@email.com', password='gabriel123', confirm_password='123gabriel')

