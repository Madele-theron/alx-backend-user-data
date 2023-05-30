#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views
# For testing this new error handler, add a new endpoint in api/v1/views/index.py:

# Route: GET /api/v1/unauthorized
# This endpoint must raise a 401 error by using abort - Custom Error Pages

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
  

@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def test_unauthorized() -> str:
  """ GET /api/v1/unauthorized
    Return:
      - raise a 401 error
    """
    return abort(401)
