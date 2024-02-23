import pytest
from sqlalchemy import create_engine


@pytest.fixture(scope="function")
def engine():
    engine = create_engine("sqlite://", echo=False)
    yield engine
    engine.dispose()
