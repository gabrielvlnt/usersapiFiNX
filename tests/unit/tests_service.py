from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import Depends, HTTPException
from schema.user import UserOut
from models.user import Users
from tests.conftest import mock_user_schema, client
from services.user import create_user, update_user
import pytest



def test_register_user_success(mock_user_schema):
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query 

    result = create_user(mock_user_schema, mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert isinstance(result, Users)

def test_register_user_error(mock_user_schema):

    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = Users(id=2)
    mock_db.query.return_value = mock_query


    with pytest.raises(HTTPException) as exc_info:
        create_user(mock_user_schema, mock_db)

    assert exc_info.value.status_code == 409
    assert "Usuário já existe" in str(exc_info.value.detail)

def test_update_user_success(mock_user_schema):
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = Users(id=1, name='Gabriel', email='test@email.com', hashed_password='$2b$12$aGu5RAJ0i4Spc6I6yvWnQuA31rZZ55rt7ktsgSjvnmak5QFLk2gK2')
    mock_db.query.return_value = mock_query

    result = update_user(1, mock_user_schema, mock_db)
    print('result:', result)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert isinstance(result, Users)

def test_update_user_error(mock_user_schema):
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query

    with pytest.raises(HTTPException) as exc_info:
        result = update_user(1, mock_user_schema, mock_db)

    assert exc_info.value.status_code == 404
    assert 'Usuário não encontrado' in str(exc_info.value.detail) 
