#!/usr/bin/python3
"""an  amenity view"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieving  the list of amenities objects"""
    listx = []
    for amenity in storage.all("Amenity").values():
        listx.append(amenity.to_dict())
    return jsonify(listx)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """retrieving  a specific amanity object"""
    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        abort(404)
    return jsonify(amenity_object.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deleteing  a specific amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_method_amaneity():
    """creating  a new amenity object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_obj(amenity_id):
    """updating  specific amenity object"""
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_instance = storage.get(Amenity, amenity_id)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_instance, key, val)
    new_instance.save()
    return jsonify(new_instance.to_dict())
