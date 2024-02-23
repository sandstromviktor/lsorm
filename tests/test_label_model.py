import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from lsorm.models import Base, Label, LabelL10n
from tests import engine

# Fixture for the session, new for each test function
@pytest.fixture(scope="function")
def session(engine):
    
    Label.metadata.create_all(engine)
    LabelL10n.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    yield Session()
    
    Session.remove()


def test_labell10n_creation():
    label = LabelL10n(label_id=1, title="Test Label", language="en")
    assert label.label_id == 1
    assert label.title == "Test Label"
    assert label.language == "en"


def test_labell10n_crud_operations(session):
    # Create
    label = LabelL10n(label_id=1, title="Test Label")
    session.add(label)
    session.commit()

    # Read
    read_label = (
        session.query(LabelL10n).filter_by(label_id=1).first()
    )
    assert read_label.title == "Test Label"
    assert read_label.language == "en"

    # Update
    read_label.title = "Updated Label"
    session.commit()
    updated_label = (
        session.query(LabelL10n).filter_by(label_id=1).first()
    )
    assert updated_label.title == "Updated Label"

    # Delete
    session.delete(updated_label)
    session.commit()
    deleted_label = (
        session.query(LabelL10n).filter_by(label_id=1).first()
    )
    assert deleted_label == None


def test_label_instance_creation():
    label = Label(id=1, lid=1, code="T", assessment_value=2, sortorder=1)
    assert label.id == 1
    assert label.lid == 1
    assert label.code == "T"
    assert label.assessment_value == 2

# Additional tests for validations and table name
def test_crud_operations(session):
    # Create
    label = Label(id=1, code="T", sortorder=1)
    session.add(label)
    session.commit()

    # Read
    read_label = session.query(Label).filter_by(id=1).first()
    assert read_label.id == 1
    assert read_label.lid == 0
    assert read_label.code == "T"
    assert read_label.assessment_value == 0

    # Update
    read_label.title = "Updated Label"
    session.commit()
    updated_label = session.query(Label).filter_by(id=1).first()
    assert updated_label.title == "Updated Label"

    # Delete
    session.delete(updated_label)
    session.commit()
    deleted_label = session.query(Label).filter_by(id=1).first()
    assert deleted_label == None
