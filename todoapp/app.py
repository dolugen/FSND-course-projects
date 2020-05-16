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

db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

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
