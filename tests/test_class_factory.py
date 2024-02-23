import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Table, Column, Integer, String
from lsorm.models import ClassFactory, Base
from settings import PREFIX

from tests import engine

# Fixture for the session, new for each test function
@pytest.fixture(scope="function")
def session(engine):
    
    test_table = Table(f'{PREFIX}_survey_123', Base.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('123X1X1', String),
                    Column('123X1X2', String),
                    Column('123X1X3', String),
                    Column('123X2X1', String),
                    # Add other columns as needed
                    )
    
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    yield Session()
    Session.remove()

def test_create_class_for_survey(session):

    factory = ClassFactory(sid=123, base_class=Base, session=session)
    SurveyClass = factory.create_class("answers")

    # Check if the SurveyClass has been created correctly
    assert hasattr(SurveyClass, 'id')
    assert hasattr(SurveyClass, 'name')
    assert hasattr(SurveyClass, '123X1X1')
    assert hasattr(SurveyClass, '123X1X2')
    assert hasattr(SurveyClass, '123X1X3')
    assert hasattr(SurveyClass, '123X2X1')
