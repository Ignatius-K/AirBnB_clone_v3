#!/usr/bin/python3
"""App file defines the API instance"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_not_found(_):
    """Handles not found route"""

    return jsonify({
        "error": "Not found"
    }), 404


@app.teardown_appcontext
def clean_up(_):
    """Cleans up the running context"""
    if not storage:
        return
    storage.close()


if __name__ == '__main__':
    from os import getenv
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', '5000')),
        threaded=True
    )
