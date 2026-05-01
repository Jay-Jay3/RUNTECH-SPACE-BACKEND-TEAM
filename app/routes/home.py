from flask import render_template, jsonify, Blueprint

bp = Blueprint("home", __name__)

@bp.route("/", methods=["GET"])
def get():
    return render_template("login.html")

@bp.route("/complaint", methods=["GET"])
def get_complaint():
    return render_template("complaint.html")

