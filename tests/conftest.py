import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import event

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.app import app
from fastapi_zero.models import table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session
    
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:', 
        connect_args={'check_same_thread': False}, 
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 5, 22)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time
    event.listen(model, 'before_insert', fake_time_hook)
    
    yield time

    event.remove(model, 'before_insert', fake_time_hook)

@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    user = User(
        username='teste',
        email='teste@teste.com',
        password='testtest'
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user