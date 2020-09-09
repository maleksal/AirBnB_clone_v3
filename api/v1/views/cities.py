#!/usr/bin/python3
''' Cities View Module
'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def retrieve_cities(state_id):
    ''' Retrieves the list of all City objects of a State
    '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    ''' Create city object linked to a state
    '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # check for formatting
    http = request.get_json()
    if not http:
        abort(400, "Not a JSON")
    if "name" not in http.keys():
        abort(400, "Missing name")
    # create city
    new_city = City(**http, state_id=state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["GET", "PUT", "DELETE"])
def RetrieveCreateDelete_city(city_id):
    ''' Retrieves a City object '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    # Handle GET request
    if request.method == "GET":
        return jsonify(city.to_dict())
    # Handle DELETE request
    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    # Handle POST request
    if request.method == "PUT":
        ignore_keys = ("id", "state_id", "created_at", "updated_at")
        http_request = request.get_json()
        if not http_request:
            abort(400, "Not a JSON")
        for attr, value in http_request.items():
            if value not in ignore_keys:
                setattr(city, attr, value)
        storage.save()
        return make_response(jsonify(city), 200)
