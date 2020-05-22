import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, items):
  '''
  Simple pagination.
  Returns a tuple with elements:
  - current page number
  - total items count (before pagination)
  - the current page items
  '''
  page = request.args.get('page', 1, type=int)
  page_size = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
  start = (page - 1) * page_size
  end = start + page_size
  return page, len(items), items[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  cors = CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response 

  
  @app.route('/questions', methods=['GET'])
  def list_questions():
    '''
    Returns a list of questions.
    Optional parameters:
    - page: Page number (default: 1)
    - limit: Page size (default: QUESTIONS_PER_PAGE)
    - searchTerm: Question string filter
    Additional return fields:
    - categories: All categories in {category_id: category_name} form
    - total_questions: Total number of questions available
    '''
    query = Question.query
    search_term = request.args.get('searchTerm')
    if search_term:
      query = query.filter(Question.question.ilike(f'%{search_term}%'))
    
    page, total_questions, questions = paginate(request, [q.format() for q in query.all()])
   
    if len(questions) == 0:
      abort(404)
    
    categories = dict([(c.id, c.type.lower()) for c in Category.query.all()])
    return jsonify({
      'success': True,
      'page': page,
      'questions': questions,
      'total_questions': total_questions,
      'categories': categories,
      'current_category': None
    })


  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    '''Returns a list of questions for a given category ID'''
    result = Question.query.filter(Question.category == category_id).all()
    result = [q.format() for q in result]
    
    return jsonify({
      'success': True,
      'questions': result
    })

  
  @app.route('/categories')
  def list_categories():
    '''Returns the list of categories'''
    categories = dict([(c.id, c.type.lower()) for c in Category.query.all()])
    return jsonify({
      'categories': categories 
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    try:
      question = Question(**request.get_json())
      question.insert()
      return jsonify({
        'success': True,
      }), 201
    except TypeError:
      abort(400)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
      'message': 'Bad Request',
      'success': False
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'message': 'Not Found',
      'success': False
    }), 404
  

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'message': 'Method Not Allowed',
      'success': False
    }), 405

  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'message': 'Unprocessable Entity',
      'success': False
    }), 422

  return app

    