import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask

from models import Question, Category, setup_db, db

'''
Writes to a SQLite database using the ORM.

The CSVs are from Postgres copy outputs:
\copy questions to 'questions.csv' csv headers;
\copy categories to 'categories.csv' csv headers;

Since the categories have non-breaking sequence of IDs,
question foreign keys match exactly.

Later the SQLite database is dumped to a *.sql file
for test purposes:
.output trivia-sqlite3-dump.sql
.dump

Why do this?
The recommended way was to configure a test Postgres database
and reset it on every test run with CLI commands.
But that's not a nice experience. With SQLite database,
it's possible to create a new database in a local file or memory
for each test case. You don't need a system service running,
no need to configure user, etc.
'''

db_path = 'sqlite:///trivia.sqlite3'

app = Flask(__name__)
setup_db(app, db_path)

categories = {}

with open('test_data/categories.csv') as cat_csv:
    cat_reader = csv.reader(cat_csv, delimiter=',')
    header = next(cat_reader)
    print(header)
    for row in cat_reader:
        cat_id, cat_name = row
        categories[cat_id] = cat_name
        db.session.add(Category(type=cat_name))
    
with open('test_data/questions.csv') as q_csv:
    q_reader = csv.reader(q_csv, delimiter=',')
    header = next(q_reader)
    print(header)
    for row in q_reader:
        _, question, answer, difficulty, category_id = row
        db.session.add(Question(question, answer, difficulty, category_id))

db.session.commit()
