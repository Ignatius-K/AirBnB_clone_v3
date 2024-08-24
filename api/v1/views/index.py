#!/usr/bin/python3
"""App_views Blueprint index"""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def get_status():
    """Gets the API status"""

    return jsonify({
        'status': 'ok'
    })


@app_views.route('/stats')
def get_stats():
    """Get the App stats"""

    stat_dict = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    response = {}
    for key, value in stat_dict.items():
        response[key] = storage.count(value)

    return jsonify(response)
