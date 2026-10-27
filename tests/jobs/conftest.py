import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine) # create the database tables
   
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db # override the get_db dependency to use the test database
    with TestClient(app) as c:
        yield c # runs the test client and yields it to the test functions

    app.dependency_overrides.clear() # clear the dependency overrides after the test is done
    Base.metadata.drop_all(bind=test_engine) # drop the database tables after the test is done
    