"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
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


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        signupUser = User.signup(username="test_user",
                                 email="test@test.com",
                                 password="HASHED_PASSWORD",
                                 image_url="")

        db.session.commit()
        self.user_id = signupUser.id

        self.client = app.test_client()

    def tearDown(self):
        """"""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        user = User.query.get(self.user_id)
        # User should have no messages & no followers
        self.assertEqual(len(user.messages), 0)
        self.assertEqual(len(user.followers), 0)

    def test_is_following(self):
        """Test is_following relationship working"""

        userTwo = User(
            email="test1@test.com",
            username="followuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(userTwo)

        db.session.commit()

        user = User.query.get(self.user_id)

        follow = Follows(user_being_followed_id=userTwo.id,
                         user_following_id=user.id)

        db.session.add(follow)
        db.session.commit()

        self.assertEqual(len(user.following), 1)
        self.assertIn(userTwo, user.following)

        # test to make see if NOT following is also working, (userTwo shouldn't be following user )
        self.assertNotIn(user, userTwo.following)

        # see if the user.followers method is functioning as expected
        self.assertEqual(len(userTwo.followers), 1)
        self.assertIn(user, userTwo.followers)

        # Does User.followers successfully detect when user is not followed by userTwo
        self.assertNotIn(userTwo, user.followers)

    def test_user_signup_success(self):
        """ Does User.signup successfully create a new user given valid credentials? """

        user = User.query.get(self.user_id)
        self.assertIsInstance(user, User)

    def test_user_signup_fail_same_username(self):
        """ Does user.signup fail to create new User when username is the same"""

        # same name as signupUser

        sameNameUser = User.signup(username="test_user",
                                   email="testTwo@testTwo.com",
                                   password="HASHED_PASSWORD",
                                   image_url="")
        with self.assertRaises(IntegrityError):
            db.session.commit()

        db.session.rollback()
        allUsers = User.query.all()

        self.assertEqual(len(allUsers), 1)

    def test_user_signup_fail_no_email(self):
        """ Does user.signup fail to create new User when email is invalid """

        with self.assertRaises(TypeError):
            invalidEmailUser = User.signup(username="invalidEmailUser",
                                           password="HASHED_PASSWORD",
                                           image_url="")

    def test_user_signup_fail_same_email(self):
        """ Does user.email fail to create new User when email is same as another user """

        signupUser = User.signup(username="same_email_user",
                                 email="test@test.com",
                                 password="HASHED_PASSWORD",
                                 image_url="")

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_authenticate_success(self):
        """ Does user.authenticate succeed to authenticate when credentials are valid """

        user = User.query.get(self.user_id)

        self.assertTrue(User.authenticate(user.username, "HASHED_PASSWORD"))

    def test_user_authenticate_fail_bad_password(self):
        """ Does user.authenticate fail to authenticate when password is invalid """

        user = User.query.get(self.user_id)

        self.assertFalse(User.authenticate(user.username, "bad password"))

    def test_user_authenticate_fail_bad_username(self):
        """ Does user.authenticate fail to authenticate when username is invalid """

        user = User.query.get(self.user_id)

        self.assertFalse(User.authenticate("bad_username", "HASHED_PASSWORD"))
