import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import func
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
    category = Category.query.get(category_id)
    if not category:
      abort(404)

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

  
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    '''Deletes a question by given id'''
    try:
      question = Question.query.get(question_id)
      if not question:
        abort(404)
      question.delete() 
      return jsonify({
        'success': True
      })
    except:
      abort(400)


  @app.route('/questions', methods=['POST'])
  def add_question():
    '''Adds a question'''
    try:
      question = Question(**request.get_json())
      question.insert()
      return jsonify({
        'success': True,
      }), 201
    except TypeError:
      abort(400)

  
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    '''Endpoint handling quiz gameplay'''
    try: 
      query = Question.query
            
      data = request.get_json()
      if data:
        previous_questions = request.get_json().get('previous_questions')
        quiz_category_id = request.get_json().get('quiz_category', {}).get('id')
        if quiz_category_id:
          category = Category.query.get(quiz_category_id)
          if category:
            query = query.filter(Question.category == category.id)
          
        if previous_questions:
          query = query.filter(Question.id.notin_(previous_questions))
      
      question = query.order_by(func.random()).first()

      if question:
        return jsonify({
          'question': question.format()
        })
      else:
        # in case there are no more questions in the category,
        # return empty response, thus ending the game
        return jsonify({
          'question': None
        })

    except Exception as err:
      print(err)
      abort(400)


  @app.errorhandler(400)
  def bad_request(error):
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

    