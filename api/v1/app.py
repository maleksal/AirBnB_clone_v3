#!/usr/bin/python3
"""
Restful api Flask Module
"""
from os import getenv
from api.v1.views import app_views
from models import storage
from flask import Flask
from flask import make_response, jsonify

# flask instance
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exce):
    ''' Calls close from storage '''
    storage.close()


@app.errorhandler(404)
def four_four_Error(e):
    ''' handle 404 Error '''
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST"),
        port=getenv("HBNB_API_PORT"),
        threaded=True)
