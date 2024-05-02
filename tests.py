from models import db, dbx, User
# DEFAULT_IMAGE_URL
from app import app
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"
os.environ["FLASK_DEBUG"] = "0"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

app.app_context().push()
db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        dbx(db.delete(User))
        db.session.commit()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.

        self.test_user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_edit_user(self):
        with app.test_client() as c:

            # user = dbx() to get the user, which can give us the id

            user_id = self.test_user_id

            response = c.post(
                f'/users/{user_id}/edit',
                data={
                    "first_name": 'changed1_first',
                    "last_name": 'changed1_last',
                    "img_url": 'www.google.com'
                },
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 302)
            response = c.get("/users")
            html = response.get_data(as_text=True)
            # TODO: follow_redirect = true, allows us to do a 200 code, test all changes
            self.assertIn("changed1_first", html)

            # TODO: future test for broken image URL

    def test_delete_user(self):
        with app.test_client() as c:

            user_id = self.test_user_id

            response = c.post(f'/users/{user_id}/delete', data={
                "user_id": 'user_id'
            })

            self.assertEqual(response.status_code, 302)
            response = c.get("/users")
            html = response.get_data(as_text=True)
            breakpoint()
            # because we can't guarantee that the teardown doesn't have before this, we'd want 2 users; each test is torn down and set up before run
            self.assertNotIn("changed1_first", html)
