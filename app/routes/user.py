from flask import Blueprint, request, jsonify, session
from app.model import User, db
# from app import db


bp = Blueprint('user', __name__)

@bp.route('/user', methods=['POST'])
def get():
    data = request.get_json()
    print("This is the dataa \n",data)
    if data['name'] or data['email'] or data['password'] or data['role'] or data['deaprtment_id'] is None:
        return jsonify({"Error": "Form not completed"}), 400
    
    if data['role'] not in ['student', 'admin']:
        return jsonify({"error": "Role must be either 'student' or 'admin'"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(name=data['name'], email=data['email'], role=data['role'])
    user.set_password(data['password'])
    print(user)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201