#!/usr/bin/python3
""" Handle Api for states"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''retrieve all states'''
    dict = {}
    listx = []
    for obj in storage.all("State").values():
        listx.append(obj.to_dict())
    return jsonify(listx)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_state_id(state_id):
    """retrieve state with id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_state(state_id):
    """delete method"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_method():
    """post methods"""
    dic = request.get_json()
    if not request.get_json():
        abort(400, desciption='Not a JSON')
    if 'name' not in dic.keys():
        abort(400, description='Missing name')

    new_state = State(**dic)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
