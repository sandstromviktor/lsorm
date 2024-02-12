import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lsorm.models import Base, LabelL10n


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

    def test_default_language(self):
        label = LabelL10n(label_id=2, title="Another Label")
        self.assertEqual(label.language, "en")

    # Additional tests for validations and table name
    def test_crud_operations(self):
        # Create
        label = LabelL10n(label_id=1, title="Test Label", language="en")
        self.session.add(label)
        self.session.commit()

        # Read
        read_label = (
            self.session.query(LabelL10n).filter_by(label_id=1).first()
        )
        assert read_label.title == "Test Label"

        # Update
        read_label.title = "Updated Label"
        self.session.commit()
        updated_label = (
            self.session.query(LabelL10n).filter_by(label_id=1).first()
        )
        assert updated_label.title == "Updated Label"

        # Delete
        self.session.delete(updated_label)
        self.session.commit()
        deleted_label = (
            self.session.query(LabelL10n).filter_by(label_id=1).first()
        )
        assert deleted_label is None


if __name__ == "__main__":
    unittest.main()
