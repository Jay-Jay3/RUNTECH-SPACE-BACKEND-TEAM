from flask import Blueprint, request, jsonify, session
from model import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if data['role'] not in ['student', 'admin']:
        return jsonify({"error": "Role must be either 'student' or 'admin'"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(name=data['name'], email=data['email'], role=data['role'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        
        session['user_id'] = user.id
        session['role'] = user.role
        return jsonify({"message": "Login successful", "role": user.role}), 200

    return jsonify({"error": "Invalid email or password"}), 401
