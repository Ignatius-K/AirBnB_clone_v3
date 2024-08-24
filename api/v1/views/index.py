"""App_views Blueprint index"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """Gets the API status"""
    return jsonify({
        'status': 'ok'
    })
