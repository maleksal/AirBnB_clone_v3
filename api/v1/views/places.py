#!/usr/bin/python3
""" Handle Api for places"""
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrieve_place_city(city_id):
    '''retrieve the corresponding place of a city'''
    if storage.get(City, city_id) is None:
        abort(404)
    citie = storage.get(City, city_id)
    return jsonify([place.to_dict() for place in citie.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_specific_place(place_id):
    '''Retrieve a specific place with it's id'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place object place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_methods(city_id):
    '''create a new Place'''
    if not storage.get(City, city_id):
        abort(404)
    if not request.get_json():
        abort(400, decription="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if not storage.get(User, request.get_json()['user_id']):
        abort(400)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    new_place['city_id'] = city.id
    new_place = Place(**request.get_json())
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False,)
def update_place_object(place_id):
    '''PUT method to update a place using id'''
    if not storage.get(Place, place_id):
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    place = request.get_json()
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at ', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
