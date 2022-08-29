import unittest
import flask
from app import create_app, db, app
from app.tests import TestConfig, create_tables


class CommentsControllerTest(unittest.TestCase):
    def setUp(self):
        # setup a test application using an in-memory database
        self.app = create_app(TestConfig)
        # self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        create_tables(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get(self):
        with app.test_client() as c:
            response = c.get('/posts/1/comments')
            self.assertEqual(response.status_code, 200)

    def test_response_struct(self):
        with app.test_client() as c:
            response = c.get('/posts/1/comments')
            test_list = list(response.get_json())
            if test_list:
                self.assertIsInstance(test_list[0], dict)
    
    def test_comments_from_not_existing_post(self):
        with app.test_client() as c:
            response = c.get('/posts/0/comments')
            test_list = list(response.get_json())
            self.assertEqual(len(test_list), 0)
    
    def test_get_users_comments(self):
        with app.test_client() as c:
            response = c.get('/users/1/comments')
            self.assertEqual(response.status_code, 200)

    def test_users_comments_struct(self):
        with app.test_client() as c:
            response = c.get('/users/1/comments')
            test_list = list(response.get_json())
            if test_list:
                self.assertIsInstance(test_list[0], dict)
                
    def test_comments_from_not_existing_user(self):
        with app.test_client() as c:
            response = c.get('/users/0/comments')
            test_list = list(response.get_json())
            self.assertEqual(len(test_list), 0)
