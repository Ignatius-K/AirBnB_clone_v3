#!/usr/bin/python3
"""View for states"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from werkzeug import exceptions


@app_views.errorhandler(400)
def handle_bad_request(response_or_exc):
    """Handle bad requests"""

    description = 'Bad Request'
    if hasattr(response_or_exc, 'description'):
        description = response_or_exc.description

    return jsonify({
        "error": description
    }), 400


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Get all states"""
    all_states = storage.all(State)
    response = []
    for state in all_states.values():
        response.append(state.to_dict())
    return jsonify(response)


@app_views.route('/states/<uuid:state_id>')
def get_state(state_id):
    """Get single state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def add_state():
    """Adds state"""
    req_body = None
    try:
        req_body = request.get_json()
    except exceptions.BadRequest:
        pass
    if not req_body:
        abort(400, description="Not valid JSON")
    state_name = req_body.get("name")
    if not state_name:
        abort(400, "Missing name")

    state = State(name=state_name)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<uuid:state_id>', methods=['PUT'])
def update_state(state_id):
    """Update the state"""
    req_body = None
    try:
        req_body = request.get_json()
    except exceptions.BadRequest:
        pass
    except exceptions.UnsupportedMediaType:
        pass
    if not req_body:
        abort(400, description="Not valid JSON")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    invalid_attr = ['id', 'created_at', 'updated_at']
    for key, value in req_body.items():
        if key not in invalid_attr:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())


@app_views.route('/states/<uuid:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete state by state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify(dict())
