from flask import Blueprint, jsonify

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "Welcome to the MLOps Project!"})
