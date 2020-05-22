from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dulguun:dulguun@localhost:5432/todoapp'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer(), primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean(), default=False)
  todolist = db.Column(db.Integer(), db.ForeignKey('todolists.id'), nullable=False)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list')


@app.route('/')
def index():
    return redirect(url_for('get_todo_list', list_id=1))

@app.route('/list/<list_id>/')
def get_todo_list(list_id):
    lists = TodoList.query.all()
    active_list=TodoList.query.get(list_id)
    todos = Todo.query.filter_by(todolist=list_id).order_by('id').all()
    return render_template('index.html', active_list=active_list, lists=lists, todos=todos)

@app.route('/new', methods=['POST'])
def add_new():
    error = False
    body = {}
    try:
        description = request.get_json().get('description')
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body = {
            'description': todo.description
        }
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed(todo_id):
    try:
        completed = request.get_json().get('completed')
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/', methods=['DELETE'])
def todo_delete(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})
