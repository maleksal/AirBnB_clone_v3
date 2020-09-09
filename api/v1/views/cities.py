#!/usr/bin/python3
''' Cities View Module
'''
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def retrieves_cities(state_id):
    ''' Retrieves the list of all City objects of a State
    '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])
