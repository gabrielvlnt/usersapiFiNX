from fastapi.testclient import TestClient
import pytest
from schema.user import UserCreate
from models.user import Users
from test_database import Base, engine
from api.v1.endpoints.user import get_db
from test_database import TestLocalSession
from main import app

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestLocalSession()
    
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def db():
    db_gen = override_get_db()
    db = next(db_gen)
    yield db
    db.close()

@pytest.fixture(autouse=True)
def delete_data_testdb():
    db: Session = TestLocalSession()
    try:
        db.query(Users).delete()
        db.commit()
        yield
    finally:
        db.close()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_user_schema():
    return UserCreate(name='Gabriel', email='test@email.com', password='gabriel123', confirm_password='123gabriel')

