import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lsorm.models import Answer, AnswerL10n, Base


class TestAnswerL10n(unittest.TestCase):
    def setUp(self):
        # Setup code for creating a database session
        engine = create_engine('sqlite://', echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        # Creating a test instance of AnswerL10n
        self.instance = AnswerL10n(id=1, aid=1, answer="test", language="en")
        self.session.add(self.instance)
        self.session.commit()

    def tearDown(self):
        # Teardown code for closing the session
        self.session.close()

    def test_create_answerl10n(self):
        # Test for creating a AnswerL10n instance
        self.assertIsNotNone(self.instance.id)

    def test_read_answerl10n(self):
        # Test for reading a AnswerL10n instance
        instance = self.session.get(AnswerL10n, self.instance.id)
        self.assertIsNotNone(instance)

    def test_update_answerl10n(self):
        # Test for updating a AnswerL10n instance
        self.instance.language = "sv"
        self.session.commit()
        updated_instance = self.session.get(AnswerL10n, self.instance.id)

        self.assertEqual(updated_instance.language, "sv")

    def test_delete_answerl10n(self):
        # Test for deleting a AnswerL10n instance
        self.session.delete(self.instance)
        self.session.commit()
        deleted_instance = self.session.get(AnswerL10n, self.instance.id)
        self.assertIsNone(deleted_instance)


class TestAnswer(unittest.TestCase):
    def setUp(self):
        # Setup code for creating a database session
        engine = create_engine("sqlite:///:memory:", echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
        # Creating a test instance of Answer
        self.instance = Answer(
            aid=1,
            qid=1,
            code="T",
            sortorder=1,
            assessment_value=2,
            scale_id=None,
        )
        self.session.add(self.instance)
        self.session.commit()

    def tearDown(self):
        # Teardown code for closing the session
        self.session.close()

    def test_create_answer(self):
        # Test for creating a Answer instance
        self.assertIsNotNone(self.instance.aid)

    def test_read_answer(self):
        # Test for reading a Answer instance
        instance = self.session.get(Answer, self.instance.aid)
        self.assertIsNotNone(instance)

    def test_update_answer(self):
        # Test for updating a Answer instance
        self.instance.assessment_value = 1
        self.session.commit()
        updated_instance = self.session.get(Answer, self.instance.aid)
        self.assertEqual(updated_instance.assessment_value, 1)

    def test_delete_answer(self):
        # Test for deleting a Answer instance
        self.session.delete(self.instance)
        self.session.commit()
        deleted_instance = self.session.get(Answer, self.instance.aid)
        self.assertIsNone(deleted_instance)


if __name__ == "__main__":
    unittest.main()
