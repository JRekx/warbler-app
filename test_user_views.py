import os
from unittest import TestCase
from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup

# Set the DATABASE_URL environmental variable for testing
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Import the app and the current user key
from app import app, CURR_USER_KEY

# Create database tables
db.create_all()

# Disable CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        # Drop and recreate the database tables
        db.drop_all()
        db.create_all()

        # Set up the Flask test client
        self.client = app.test_client()

        # Create a test user
        self.testuser = User.signup(
            username='Testy',
            email='testmctest@testy.com',
            password='tesuser',
            image_url=None
        )

        # Set a test user ID
        self.testuser_id = 5454
        self.testuser.id = self.testuser_id

        # Create additional test users
        self.u1 = User.signup('jjr', 'testytest@gmail.com', 'password', None)
        self.u1_id = 788
        self.u1.id = self.u1_id
        self.u2 = User.signup('xxy', 'testing2@gmail.com', 'password', None)
        self.u2.id = 1826
        self.u2_id = self.u2.id
        self.u3 = User.signup('jrek', 'mctesty@gmail.com', 'password', None)
        self.u4 = User.signup("testing", "test4@test.com", "password", None)

        # Commit the changes to the database
        db.session.commit()

    def tearDown(self):
        """Rollback the session after each test."""
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_index(self):
        """Test the users index page."""

        with self.client as c:
            resp = c.get('/users')

            # Check if user profiles are present in the response
            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@jjr", str(resp.data))
            self.assertIn("@xxy", str(resp.data))
            self.assertIn("@jrek", str(resp.data))
            self.assertIn("@testing", str(resp.data))

    def test_user_show(self):
        """Test the user show page."""

        with self.client as c:
            resp = c.get(f'/users/{self.testuser_id}')
            
            # Check if the user's profile is present in the response
            self.assertEqual(resp.status_code, 200)
            self.assertIn('@testuser', str(resp.data))
