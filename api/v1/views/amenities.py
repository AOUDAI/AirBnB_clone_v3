#!/usr/bin/python3
""" Handles amenity objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/')
def get_amenities():
    '''Retrieves a list of all Amenity objects'''

    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    ''' Retrieves an Amenity object'''

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    ''' Deletes an Amenity object'''

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    ''' Creates an Amenity'''

    try:
        data = request.get_json()
    except Exception as error:
        abort(400, 'Not a JSON')
    
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')

    newAmenity = Amenity(name=name)
    storage.new(newAmenity)
    storage.save()

    return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    ''' Updates an Amenity object'''

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    try:
        newData = request.get_json()
    except Exception as error:
        abort(400, 'Not a JSON')

    for key, value in newData.items():
        if key not in ['created_at', 'updated_at', 'id']:
            amenity.__setattr__(key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200