from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import Depends, HTTPException
from schema.user import UserCreate, UserOut
from models.user import Users
from api.v1.endpoints.user import create_user
import pytest


def test_register_user(client):
    payload = {
        'name': 'Daniel Lima',
        'email': 'daniel@abacatepay.com',
        'password': 'abacatepay123',
        'confirm_password': 'abacatepay123'
    }

    response = client.post('/user/register', json=payload)

    assert response.status_code == 201
    assert response.json()['email'] == 'daniel@abacatepay.com'