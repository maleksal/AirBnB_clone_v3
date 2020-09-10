#!/usr/bin/python3
"""
Link Place and Amenity vue Module
"""
from os import getenv
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def retrieve_amenity_place(place_id):
    """ Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=["DELETE"], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """ Deletes Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    amenity_pointer = None
    if place and amenity:
        if amenity in place.amenities:
            storage.delete(amenity)
            storage.save()
            return jsonify({})
        abort(404)
    abort(404)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """ Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
    abort(404)
