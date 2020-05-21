import os
import unittest
import tempfile
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # designate a temporary file to use as sqlite3
        self._db_fd, self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app.config['TESTING'] = True
        self.database_path = f"sqlite:///{self.app.config['DATABASE']}"
        setup_db(self.app, self.database_path)

        # populate the test database with data
        with self.app.app_context():
            self.db = SQLAlchemy(self.app)
            self.db.create_all()
            with self.app.open_resource('../test_data/trivia-sqlite3-inserts.sql') as f:
                for line in f.readlines():
                    self.db.engine.execute(line.decode('utf8'))

    
    def tearDown(self):
        # cleanup the test database
        os.close(self._db_fd)
        os.unlink(self.app.config['DATABASE'])

    def test_get_questions(self):
        '''Test the list of questions'''
        response = self.client.get('/questions')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # number of questions in the test database
        self.assertEqual(data['total_questions'], 19)
        self.assertGreater(len(data['questions']), 0)
        self.assertIn('categories', data)
        self.assertIn('current_category', data)
    
    def test_get_questions_pagination(self):
        '''Test pagination with default page size'''
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
    
    def test_page_size_small(self):
        '''Test request with a small page size'''
        pass
    
    def test_questions_by_category(self):
        response = self.client.get('/categories/1/questions')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data['questions']), 0)
    
    def test_questions_from_nonexistent_category(self):
        pass
    
    def test_list_categories(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data['categories']), 0)
    
    def test_add_categories(self):
        '''is this in scope? if not test that 405 is returned'''
    
    def test_search(self):
        response = self.client.get(f'/questions?searchTerm=movie')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data['questions']), 0)
        for question in data['questions']:
            self.assertIn('movie', question['question'].lower())
    
    def test_search_empty(self):
        '''Test search for a non-existing question'''
        pass
    
    def test_add_question(self):
        questions_initial = self.client.get('/questions').get_json()
        # make note how many questions there are 
        total_questions_initial = questions_initial['total_questions']

        # non-trivia alert!
        question = {
            'question': 'If a tree falls in a forest and no one is around to hear it, does it make a sound?',
            'answer': 'It depends on how you look at it.',
            'difficulty': 3,
            'category': 1,
        }
        response = self.client.post('/questions', json=question)
        self.assertEqual(response.status_code, 201)
        
        result = self.client.get('/questions?limit=100').get_json()
        # the count was incremented
        self.assertEqual(result['total_questions'], total_questions_initial + 1)
        # the last question is the one we added
        self.assertEqual(question['question'], result['questions'][-1]['question'])
    
    def test_add_question_bad_request(self):
        '''Test that adding a question while missing fields fails'''
        pass
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(verbosity=2)