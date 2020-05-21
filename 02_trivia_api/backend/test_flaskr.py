import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://dulguun:dulguun@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # TODO: truncate tables and load trivia.psql
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        response = self.client.get('/questions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # number of questions in the test database, source: ./trivia.psql
        self.assertEqual(data['total_questions'], 19)
        self.assertGreater(len(data['questions']), 0)
        self.assertIn('categories', data)
        self.assertIn('current_category', data)
    
    def test_get_questions_pagination(self):
        response_page1 = self.client.get('/questions?page=1')
        self.assertEqual(response_page1.status_code, 200)
        data = json.loads(response_page1.data)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 10)

        response_page2 = self.client.get('/questions?page=2')
        self.assertEqual(response_page2.status_code, 200)
        data = json.loads(response_page2.data)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 9)

        response_page2 = self.client.get('/questions?page=3')
        self.assertEqual(response_page2.status_code, 404)
        data = json.loads(response_page2.data)
        self.assertEqual(data['message'], 'Not found')
        self.assertFalse(data['success'])
    
    def test_questions_by_category(self):
        response = self.client.get('/categories/1/questions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data['questions']), 0)
    
    def test_list_categories(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data['categories']), 0)
    
    def test_search(self):
        response = self.client.post('/questions', data={'searchTerm': 'movie'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data['questions']), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()