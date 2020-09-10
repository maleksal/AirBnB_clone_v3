#!/usr/bin/python3
"""
User  View Module

"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_users():
    """ Retrieving  all user object
    """
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieving  user object with id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user_object(user_id):
    """ deleting  user object refrenced by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user_object():
    """ Creating  user object
    """
    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")
    for key in ["email", "password"]:
        if key not in http_request.keys():
            abort(400, "Missing {}".format(key))
    user = User(**http_request)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user_object(user_id):
    """ updating  user opject refrenced by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")
    for attr, value in http_request.items():
        if attr not in ["id email", "created_at", "updated_at"]:
            setattr(user, attr, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
