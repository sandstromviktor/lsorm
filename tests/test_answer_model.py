import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from lsorm.models import Answer, AnswerL10n, Base

from tests import engine

# Fixture for the session, new for each test function
@pytest.fixture(scope="function")
def session(engine):
    
    Answer.metadata.create_all(engine)
    AnswerL10n.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    yield Session()
    
    Session.remove()

def test_answerl10n_creation():
    answer = AnswerL10n(id=1, aid=2, answer="Test Answer", language="en")
    assert answer.id == 1
    assert answer.aid == 2
    assert answer.answer == "Test Answer"
    assert answer.language == "en"


def test_answerl10n_crud_operations(session):
    # Create
    answer = AnswerL10n(id=1, aid=2, answer="Test Answer", language="en")
    session.add(answer)
    session.commit()

    # Read
    read_answer = (
        session.query(AnswerL10n).filter_by(id=1, aid=2).first()
    )
    assert read_answer.answer == "Test Answer"
    assert read_answer.language == "en"

    # Update
    read_answer.answer = "Updated Answer"
    read_answer.aid = 3
    session.commit()
    updated_answer = (
        session.query(AnswerL10n).filter_by(id=1, aid=3).first()
    )
    assert updated_answer.answer == "Updated Answer"

    # Delete
    session.delete(updated_answer)
    session.commit()
    deleted_answer = (
        session.query(AnswerL10n).filter_by(id=1).first()
    )
    assert deleted_answer == None


def test_answerl10n_non_nullable_field(session):
    # Try to create AnswerL10n object with a non-nullable field being null
    with pytest.raises(Exception):
        answer = AnswerL10n(id=1, aid=2, answer=None, language="en")
        session.add(answer)
        session.commit()
        
        

def test_answer_creation():
    answer = Answer(aid=1, qid=2, code="abcde", sortorder=1)
    assert answer.aid == 1
    assert answer.qid == 2
    assert answer.code == "abcde"
    assert answer.sortorder == 1


def test_answer_crud_operations(session):
    # Create
    answer = Answer(aid=1, qid=2, code="abcde", sortorder=1)
    session.add(answer)
    session.commit()

    # Read
    read_answer = (
        session.query(Answer).filter_by(aid=1, qid=2).first()
    )
    assert read_answer.code == "abcde"
    assert read_answer.assessment_value == 0
    assert read_answer.scale_id == 0

    # Update
    read_answer.code = "ABCDE"
    read_answer.qid = 3
    session.commit()
    updated_answer = (
        session.query(Answer).filter_by(aid=1, qid=3).first()
    )
    assert updated_answer.code == "ABCDE"

    # Delete
    session.delete(updated_answer)
    session.commit()
    deleted_answer = (
        session.query(Answer).filter_by(aid=1, qid=3).first()
    )
    assert deleted_answer == None


def test_answer_non_nullable_field(session):
    # Try to create AnswerL10n object with a non-nullable field being null
    with pytest.raises(Exception):
        answer = Answer(aid=1, qid=2, code=None, sortorder=1)
        session.add(answer)
        session.commit()