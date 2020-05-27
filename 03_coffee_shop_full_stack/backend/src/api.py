import os
from functools import wraps
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from jose import jwt

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
# db_drop_and_create_all()


# ROUTES
@app.route("/drinks")
def get_drinks():
    """Returns list of drinks. Publically viewable."""
    result = {
        "success": True,
        "drinks": [drink.short() for drink in Drink.query.all()],
    }
    return jsonify(result)


@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail(jwt):
    """
    Returns list of drinks with details.
    Requires authentication and permission
    """
    result = {
        "success": True,
        "drinks": [drink.long() for drink in Drink.query.all()],
    }
    return jsonify(result)


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def add_drink(jwt):
    """Adds a drink. Requires authentication and permission"""
    data = request.get_json()
    if not data or "title" not in data or "recipe" not in data:
        abort(400)

    if type(data["recipe"]) != list:
        # expected shape: [ { ... } ]
        abort(400)

    drink = Drink(title=data["title"], recipe=json.dumps(data["recipe"]))
    drink.insert()
    return jsonify({"success": True, "drinks": [drink.long()]})


@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(jwt, drink_id):
    """Update a drink. Requires authentication and permission"""
    drink = Drink.query.get(drink_id)
    if not drink:
        abort(404)

    data = request.get_json()
    if not data or ("title" not in data and "recipe" not in data):
        abort(400)

    if "title" in data:
        drink.title = request.get_json()["title"]
    if "recipe" in data:
        drink.recipe = json.dumps(request.get_json()["recipe"])
    drink.update()
    return jsonify({"success": True, "drinks": [drink.long()]})


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(jwt, drink_id):
    """Deletes a drink. Requires authentication and permission"""
    drink = Drink.query.get(drink_id)
    if not drink:
        abort(404)

    drink.delete()
    return jsonify({"success": True, "delete": drink_id})


# Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify({"success": False, "error": 400, "message": "bad request"}),
        400,
    )


@app.errorhandler(401)
def unauthorized(error):
    return (
        jsonify({"success": False, "error": 401, "message": "unauthorized request"}),
        401,
    )
