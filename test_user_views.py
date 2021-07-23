"""User views tests."""
# TODO need to add testing here for user views

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app, CURR_USER_KEY
from flask import session, g

import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewsTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        current_user = User.signup(username="test_user",
                                   email="test@test.com",
                                   password="HASHED_PASSWORD",
                                   image_url="")

        user1 = User.signup(username="test_user1",
                            email="test1@test.com",
                            password="HASHED_PASSWORD",
                            image_url="")

        user2 = User.signup(username="test_user2",
                            email="test2@test.com",
                            password="HASHED_PASSWORD",
                            image_url="")

        db.session.commit()

        follow1 = Follows(user_being_followed_id=user1.id,
                          user_following_id=current_user.id)

        follow2 = Follows(user_being_followed_id=current_user.id,
                          user_following_id=user2.id)

        db.session.add(follow1)
        db.session.add(follow2)

        db.session.commit()

        self.user_id = current_user.id

        with app.app_context():
            g.user = current_user

        self.client = app.test_client()

    def tearDown(self):
        """"""
        db.session.rollback()

    # def test_follower_following_views(self):
    #     """ """

    #     with app.test_client() as client:
    #         resp = client.get('/users/<int:user_id>/following')
    #         html = resp.get_data(as_text = True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("test_user2", html)
