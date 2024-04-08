#!/usr/bin/python3

from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from models import storage
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def storage_hundler(exception):
    """ calls close method of storage object"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handles not found error"""
    return make_response(jsonify({"error": "Not found"}))



# @app.errorhandler(400)
# def bad_request(error):
#     """ Handles Bad request error"""
#     return jsonify({'error': str(error)})

if __name__ == "__main__":

    hostName = environ.get('HBNB_API_HOST')
    portNumber = environ.get('HBNB_API_PORT')
    if hostName is None:
        hostName = '0.0.0.0'
    if portNumber is None:
        portNumber = 5000

    app.run(host=hostName, port=portNumber, threaded=True, debug=True)
