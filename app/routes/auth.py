# from flask import request, jsonify, Blueprint

# bp = Blueprint('user', __name__)

# @bp.route("/auth/register", methods=["POST"])
# def allUsers():
#     data = request.get_json()
#     return 

# @bp.route("/auth/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     return 

# @bp.route("/auth/logout", methods=["POST"])
# def logout():
#     data = request.get_json()
#     return 

from flask import Blueprint, request, url_for,jsonify, session, render_template, redirect
from app.model import User, db
from app.schema import isValidEmail 
# from app import db


bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET'])
def get_register():
    return render_template('register.html')

@bp.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    isValidEmail(data['email'])
    if data['role'] not in ['student', 'admin']:
        return jsonify({"error": "Role must be either specified"}), 400
    if User.query.filter_by(email=data['email']).first():
        return redirect(url_for("auth.get_login"))
        # return jsonify({"error": "Email already registered"}), 400

    user = User(
        name=data['name'], 
        email=data['email'], 
        role=data['role'], 
        )
    user.set_password(data['password'])
    print(user)

    db.session.add(user)
    db.session.commit()

    return redirect("/login", 201)

@bp.route('/login', methods=["GET"])
def get_login():
    return render_template("login.html")

@bp.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        session['role'] = user.role
        print(user.id)
        return jsonify({"message": "Login successful", "role": user.role}), 200
    return jsonify({"error": "Invalid email or password"}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    return