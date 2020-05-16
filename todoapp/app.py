from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dulguun:dulguun@localhost:5432/todoapp'
db = SQLAlchemy(app)

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
    description = request.form.get('description')
    db.session.add(Todo(description=description))
    db.session.commit()
    return redirect(url_for('index'))
