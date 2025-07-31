from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import Depends
from schema.user import UserCreate
from models.user import Users
from main import app
from api.v1.endpoints import get_db

client = TestClient(app)


@pytest.fixture
def override_get_db():
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = Usuario(id=1, name='Gabriel')
    yield Session

@pytest.fixture
def mock_user_schema():
    return UserCreate(name='Gabriel', email='test@email.com', password='123gabriel', confirm_password='123gabriel')

client.dependency_overrides[get_db] = override_get_db


def test_register_user(mock_user_schema, override_get_db):
    