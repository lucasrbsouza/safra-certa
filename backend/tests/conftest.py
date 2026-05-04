import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.core.database as db_module
from app.core.database import Base
from app.core.dependencies import get_commodity_gateway, get_db
from app.gateways.mock_commodity_gateway import MockCommodityGateway

TEST_DATABASE_URL = "sqlite:///./test.db"

_test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

# Override globals before app is imported so no postgres connection is attempted
db_module._engine = _test_engine
db_module._SessionLocal = _TestingSessionLocal


from main import app  # noqa: E402 — must come after db override


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=_test_engine)
    yield
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture
def db_session():
    connection = _test_engine.connect()
    transaction = connection.begin()
    session = _TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_gateway():
    return MockCommodityGateway(randomize=False)


@pytest.fixture
def client(db_session):
    def override_db():
        yield db_session

    def override_gateway():
        return MockCommodityGateway(randomize=False)

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_commodity_gateway] = override_gateway
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
