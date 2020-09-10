#!/usr/bin/python3
"""
Review vue Module
"""
from models.place import Place
from models.review import Review
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def retrieve_reviews_by_id(place_id):
    ''' Retrieves the list of all Review objects of a Place
    '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_review_object(review_id):
    ''' Retrieves a Review object refrenced by id
    '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_object(review_id):
    ''' deletes a Review object refrenced by id
    '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['DELETE'],
                 strict_slashes=False)
def create_review_object(place_id):
    ''' create a review object
    '''
    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")
    for key_name in ["user_id", "text"]:
        if key_name not in http_request.keys():
            abort(400, "Missing {}".format(key_name))
    place = storage.get(Place, place_id)
    user = storage.get(User, http_request["user_id"])
    if not place or not user:
        abort(404)
    http_request["place_id"] = place_id
    review = Review(**http_request)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review_object(review_id):
    ''' updates a Review object refrenced by id
    '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    http_request = request.get_json()
    if not http_request:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for attr, value in http_request.items():
        if attr not in ignore_keys:
            setattr(review, attr, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
