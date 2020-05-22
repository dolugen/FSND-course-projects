# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Test Dependencies

For testing, [SQLite3](https://sqlite.org/index.html) database is used.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. Change the owner name in the file to your database user.

From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

### `GET /categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns:
  - `200 OK` response with an object with a single key, categories, that contains a object of id: category_string key:value pairs. 

Example response:
```js
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}
```

### `GET /categories/<category_id>/questions`
- Returns an object that contains a list of questions for the given category.
- Request Path Arguments: `category_id`
- Returns:
  - `200 OK` response with an object with a single key, questions, with value as an array of question objects.
  - `404 Not Found` response when an unknown category ID was provided.

Example response:
```js
{
    'questions': [
        {
            'id': 1,
            'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
            'answer': "Maya Angelou",
            'category': 2,
            'difficulty': 4
        }
    ]
}
```

### `GET /questions`
- Returns an object that contains questions.
- Request Arguments:
  - `page`: Page number (optional, default: 1)
  - `limit`: Page size (optional, default: 10)
  - `searchTerm`: Question string filtering value
- Returns:
  - `200 OK` response with an object that contains questions and other values:
    - `page`: Current page number
    - `questions`: The question objects array
    - `total_questions`: The total available questions
    - `categories`: Object mapping of all categories in {id: name} form
  - `404 Not Found` response when the given filter arguments produce no result.

Example response:
```js
{
    'questions': [
        {
            'id': 1,
            'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
            'answer': "Maya Angelou",
            'category': 2,
            'difficulty': 4
        }
    ],
    'page': 1,
    'total_questions': 100,
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    }
}
```

### `POST /questions`
- Adds a new question. Accepts a question object.
- Request Body:
  - `question`: Question string
  - `answer`: Answer string
  - `category`: Category ID
  - `difficulty`: Difficulty score
- Returns:
  - `201 Created` response when a new record was successfully created.
  - `400 Bad Request` response when any of the fields are missing.

Example request:
```js
{
    'question': "New question string",
    'answer': "The answer string",
    'category': 2,
    'difficulty': 4
}
```

### `DELETE /questions/<question_id>`
- Deletes a question from the app.
- Request Path Arguments: `question_id`
- Returns:
  - `200 OK` response when the question was deleted.
  - `404 Not Found` response when an unknown question was specified.
  - `400 Bad Request` response if given argument was invalid.

### `POST /quizzes`
- Handles the quiz gameplay, provides questions.
- Request body:
  - `previous_questions`: Array of question IDs that the player already seen (optional)
  - `quiz_category`: Question category ID (optional)
- Returns:
  - `200 OK` response with an object with one key, question, that contains a question object.
  - `400 Bad Request` response when a request parameter is invalid.

Example request:
```js
{
    'previous_questions': [1,2,3],
    'quiz_category': 1
}
```

Example response:
```js
{
    'question': {
        'id': 1,
        'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        'answer': "Maya Angelou",
        'category': 2,
        'difficulty': 4
    }
}
```


## Testing
To run the tests, run
```
python test_flaskr.py
```