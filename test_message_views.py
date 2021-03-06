"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, connect_db, Message, User

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

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_add_message_as_other_user_fail(self):
        """Can't add a message as user not signed in"""
        # TODO need to complete this test

    def test_add_message_as_loggedout_user_fail(self):
        """ test logged out user cannot add a new message"""
        with self.client as c:
            resp = c.post("/messages/new",
                          data={"text": "Hello"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Access unauthorized", html)

    def test_delete_message_as_loggedout_user_fail(self):
        """ test logged out user cant delete message """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # save post response of new message instance with text of "DELETE ME"
            resp = c.post("/messages/new", data={"text": "DELETE ME"})
            self.msg = Message.query.one()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = None

            delete_resp = c.post(
                f"messages/{self.msg.id}/delete", follow_redirects=True)
            html = delete_resp.get_data(as_text=True)

            self.assertIn("Access unauthorized", html)

    def test_delete_message(self):
        """ Can delete message posted by signed in user """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # save post response of new message instance with text of "DELETE ME"
            resp = c.post("/messages/new", data={"text": "DELETE ME"})
            msg = Message.query.one()

            # save post response of deletion of "DELETE ME" message
            delete_resp = c.post(
                f"/messages/{msg.id}/delete", follow_redirects=True)

            # test for successful render template after deletion
            self.assertEqual(delete_resp.status_code, 200)

            # tests previous message body text NOT IN html (prove its been deleted)
            html = delete_resp.get_data(as_text=True)
            self.assertNotIn("DELETE ME", html)

    def test_delete_other_users_message_fail(self):
        """ Cant delete message posted by user not signed in """
        # TODO need to complete this test
