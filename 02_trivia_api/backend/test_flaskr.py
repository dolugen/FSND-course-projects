import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
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
            # TODO: configure Sqlite
            # TODO: load trivia.psql
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        # TODO: drop sqlite
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        response = self.client.get('/questions')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # number of questions in the test database, source: ./trivia.psql
        self.assertEqual(data['total_questions'], 19)
        self.assertGreater(len(data['questions']), 0)
        self.assertIn('categories', data)
        self.assertIn('current_category', data)
    
    def test_get_questions_pagination(self):
        response_page1 = self.client.get('/questions?page=1')
        self.assertEqual(response_page1.status_code, 200)
        data = response_page1.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 10)

        response_page2 = self.client.get('/questions?page=2')
        self.assertEqual(response_page2.status_code, 200)
        data = response_page2.get_json()
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 9)

        response_page3 = self.client.get('/questions?page=3')
        self.assertEqual(response_page3.status_code, 404)
        data = response_page3.get_json()
        self.assertEqual(data['message'], 'Not found')
        self.assertFalse(data['success'])
    
    def test_page_size(self):
        '''Test page size overriding with limit'''
        response = self.client.get('/questions?page=1&limit=100')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['total_questions'], len(data['questions']))

        # Since page size is larger than our dataset,
        # there's nothing on the second page
        response = self.client.get('/questions?page=2&limit=100')
        self.assertEqual(response.status_code, 404)
    
    def test_questions_by_category(self):
        response = self.client.get('/categories/1/questions')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data['questions']), 0)
    
    def test_list_categories(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data['categories']), 0)
    
    def test_search(self):
        response = self.client.get(f'/questions?searchTerm=movie')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data['questions']), 0)
        for question in data['questions']:
            self.assertIn('movie', question['question'].lower())
    
    def test_add_question(self):
        questions_initial = self.client.get('/questions').get_json()
        total_questions_initial = questions_initial['total_questions']

        question = {
            'question': 'If a tree falls in a forest and no one is around to hear it, does it make a sound?',
            'answer': 'It depends on how you look at it.',
            'difficulty': 3,
            'category': 1,
        }
        response = self.client.post('/questions', json=question)
        self.assertEqual(response.status_code, 201)
        
        questions = self.client.get('/questions').get_json()
        self.assertEqual(questions['total_questions'], total_questions_initial + 1)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(verbosity=2)