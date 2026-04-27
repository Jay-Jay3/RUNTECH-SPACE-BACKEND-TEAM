from flask import request, jsonify, Blueprint

bp = Blueprint('user', __name__)

@bp.route("/auth/register", methods=["POST"])
def allUsers():
    data = request.get_json()
    return 

@bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    return 

@bp.route("/auth/logout", methods=["POST"])
def logout():
    data = request.get_json()
    return 

