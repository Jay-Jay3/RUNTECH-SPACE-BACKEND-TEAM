from flask import Blueprint, request, jsonify, session
from model import db, Complaint
from decorators import login_required, admin_required
from flask import render_template

complaints_bp = Blueprint('complaints', __name__)

@complaints_bp.route('/complaints/submit', methods=['POST'])
@login_required
def submit_complaint():
    data = request.get_json()
    complaint = Complaint(
        title=data['title'],
        description=data['description'],
        user_id=1
    )
    db.session.add(complaint)
    db.session.commit()
    return jsonify({"message": "Complaint submitted successfully"}), 201

@complaints_bp.route('/complaints/all', methods=['GET'])
@admin_required
def view_all_complaints():
    complaints = Complaint.query.all()
    results = [
        {"id": c.id, "title": c.title, "description": c.description, "user_id": c.user_id}
        for c in complaints
    ]
    return jsonify(results), 200

@complaints_bp.route('/complaints/update/<int:complaint_id>', methods=['PUT'])
@admin_required
def update_complaint(complaint_id):
    data = request.get_json()
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = data.get('status', complaint.status)
    db.session.commit()
    return jsonify({"message": "Complaint updated successfully", "status": complaint.status}), 200

@complaints_bp.route('/complaints/My_complaints', methods=['GET'])
@login_required
def view_my_complaints():
    user_id = session.get('user_id')
    complaints = Complaint.query.filter_by(user_id=user_id).all()
    results = [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "status": c.status,
            "created_at": c.created_at,
            "updated_at": c.updated_at
        }
        for c in complaints
    ]
    return jsonify(results), 200


@complaints_bp.route('/complaints/mine/view')
@login_required
def student_dashboard():
    user_id = session.get('user_id')
    complaints = Complaint.query.filter_by(user_id=user_id).all()
    return render_template("student_dashboard.html", complaints=complaints)

