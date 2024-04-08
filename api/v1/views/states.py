#!/usr/bin/python3
""" For state opjects"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def states():
    """ Get all State objects"""
    allStates = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(allStates)


@app_views.route('/states/<state_id>', methods=['GET'])
def state(state_id):
    """ Get a state for the given state id"""
    myState = storage.get(State, state_id)
    if myState is None:
        abort(404)
    return jsonify(myState.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a state object identified by state_id"""
    myState = storage.get(State, state_id)
    if myState is None:
        abort(404)
    storage.delete(myState)
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'])
def post():
    """ Create a new State"""
    try:
        data = request.get_json()
    except Exception as error:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')

    newState = State(name=name)
    storage.new(newState)
    storage.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Update the state objects corresponde to state id"""

    myState = storage.get(State, state_id)
    if myState is None:
        abort(404)

    try:
        newData = request.get_json()
    except Exception as error:
        abort(400, 'Not a JSON')

    for key, value in newData.items():
        if key not in ['created_at', 'updated_at', 'id']:
            myState.__setattr__(key, value)

    storage.save()
    return jsonify(myState.to_dict()), 200
