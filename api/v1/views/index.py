#!/usr/bin/python3
"""
a  routes module
"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status", methods=['GET'])
def status():
    ''' returning  status code of the api '''
    return jsonify(status="OK")


@app_views.route("/stats", methods=['GET'])
def stats():
    '''returning  stats of objects'''
    dict = {}
    for key, cls in classes.items():
        dict[key] = storage.count(cls)
    return jsonify(dict)
