import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lsorm.models import Base, Label, LabelL10n


class TestLabelL10n(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite:///:memory:"
        )  # Use in-memory SQLite database
        Session = sessionmaker(bind=engine)
        self.session = Session()

        Base.metadata.create_all(engine)

    def test_instance_creation(self):
        label = LabelL10n(label_id=1, title="Test Label", language="en")
        self.assertEqual(label.label_id, 1)
        self.assertEqual(label.title, "Test Label")
        self.assertEqual(label.language, "en")

    # Additional tests for validations and table name
    def test_crud_operations(self):
        # Create
        label = LabelL10n(label_id=1, title="Test Label")
        self.session.add(label)
        self.session.commit()

        # Read
        read_label = (
            self.session.query(LabelL10n).filter_by(label_id=1).first()
        )
        self.assertEqual(read_label.title, "Test Label")
        self.assertEqual(read_label.language, "en")

        # Update
        read_label.title = "Updated Label"
        self.session.commit()
        updated_label = (
            self.session.query(LabelL10n).filter_by(label_id=1).first()
        )
        self.assertEqual(updated_label.title, "Updated Label")

        # Delete
        self.session.delete(updated_label)
        self.session.commit()
        deleted_label = (
            self.session.query(LabelL10n).filter_by(label_id=1).first()
        )
        self.assertIsNone(deleted_label)


class TestLabel(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite:///:memory:"
        )  # Use in-memory SQLite database
        Session = sessionmaker(bind=engine)
        self.session = Session()

        Base.metadata.create_all(engine)

    def test_instance_creation(self):
        label = Label(id=1, lid=1, code="T", assessment_value=2, sortorder=1)
        self.assertEqual(label.id, 1)
        self.assertEqual(label.lid, 1)
        self.assertEqual(label.code, "T")
        self.assertEqual(label.assessment_value, 2)

    # Additional tests for validations and table name
    def test_crud_operations(self):
        # Create
        label = Label(id=1, code="T", sortorder=1)
        self.session.add(label)
        self.session.commit()

        # Read
        read_label = self.session.query(Label).filter_by(id=1).first()
        self.assertEqual(read_label.id, 1)
        self.assertEqual(read_label.lid, 0)
        self.assertEqual(read_label.code, "T")
        self.assertEqual(read_label.assessment_value, 0)

        # Update
        read_label.title = "Updated Label"
        self.session.commit()
        updated_label = self.session.query(Label).filter_by(id=1).first()
        self.assertEqual(updated_label.title, "Updated Label")

        # Delete
        self.session.delete(updated_label)
        self.session.commit()
        deleted_label = self.session.query(Label).filter_by(id=1).first()
        self.assertIsNone(deleted_label)


if __name__ == "__main__":
    unittest.main()
