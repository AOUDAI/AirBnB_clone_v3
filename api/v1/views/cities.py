#!/usr/bin/python3
""" Handles all default RESTFull API for City objects"""


from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities')
def cities_of_state(state_id):
    """ Retrieves the list of all City objects of a State"""

    myState = storage.get(State, state_id)

    if myState is None:
        abort(404)

    myCities = [city.to_dict() for city in myState.cities]

    return jsonify(myCities)


@app_views.route('/cities/<city_id>')
def get_city(city_id):
    """ Retrieves a City object."""

    myCity = storage.get(City, city_id)
    
    if myCity is None:
        abort(404)
    
    return jsonify(myCity.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a City object"""

    myCity = storage.get(City, city_id)

    if myCity is None:
        abort(404)
    
    storage.delete(myCity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Creates a City"""

    myState = storage.get(State, state_id)

    if myState is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, 'Not a JSON')
    
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')

    newCity = City(name=name, state_id=state_id)
    storage.new(newCity)
    storage.save()

    return jsonify(newCity.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Update the city object corresponde to city id"""

    myCity = storage.get(City, city_id)
    if myCity is None:
        abort(404)

    try:
        newData = request.get_json()
    except Exception as error:
        abort(400, 'Not a JSON')

    for key, value in newData.items():
        if key not in ['created_at', 'updated_at', 'id']:
            myCity.__setattr__(key, value)

    storage.save()
    return jsonify(myCity.to_dict()), 200
    
