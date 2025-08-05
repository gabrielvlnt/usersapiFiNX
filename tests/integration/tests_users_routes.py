from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import Depends, HTTPException
from schema.user import UserCreate, UserOut
from models.user import Users
from test_database import engine
from tests.conftest import delete_data_testdb
from main import app
from api.v1.endpoints.user import create_user
import pytest


def test_register_user(client):

    payload = {
        'name': 'Israel Lima',
        'email': 'israelson@abacatepay.com',
        'password': 'abacatepay123',
        'confirm_password': 'abacatepay123'
    }

    response = client.post(f'/user/register/', json=payload)

    assert response.status_code == 201
    assert response.json()['email'] == 'israelson@abacatepay.com'

def test_update_profile(client, db):
    fake_user = Users(name='Gabriel', email='gabriel@email.com', hashed_password='$2b$12$QIDjYGoko7t7Q2Ia9tI.8uk.5iLK5WiICcnzPKRdE/Oaji7mR2UEi')
    db.add(fake_user)
    db.commit()
    
    payload = {
        'name': 'Gabiru Lima',
        'email': 'israelson@abacatepay.com',
        'password': 'string',
        'confirm_password': 'string'
    }

    response = client.put(f'/user/update_profile/{fake_user.id}', json=payload)

    assert response.status_code == 201
    assert response.json()['email'] == 'israelson@abacatepay.com'

def test_delete_user(client, db):
    fake_user = Users(name='Gabriel', email='gabriel@email.com', hashed_password='$2b$12$QIDjYGoko7t7Q2Ia9tI.8uk.5iLK5WiICcnzPKRdE/Oaji7mR2UEi')
    db.add(fake_user)
    db.commit()

    payload = {
        'name': 'Gabiru Lima',
        'email': 'israelson@abacatepay.com',
        'password': 'string',
        'confirm_password': 'string'
    }

    response = client.delete(f'/user/delete_profile/{fake_user.id}')

    assert response.status_code == 204

def test_login_token(client, db):
    fake_user = Users(name='Gabriel', email='gabriel@email.com', hashed_password='$2b$12$QIDjYGoko7t7Q2Ia9tI.8uk.5iLK5WiICcnzPKRdE/Oaji7mR2UEi')
    db.add(fake_user)
    db.commit()

    payload = {
        'username': 'gabriel@email.com',
        'password': 'string'
    }

    response = client.post('/user/token', data=payload)

    assert response.status_code == 202
    data = response.json()
    assert 'access_token' in data
    print(data)