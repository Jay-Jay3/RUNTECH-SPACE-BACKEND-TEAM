# This is the file that will house

from flask import Blueprint, request, url_for,jsonify, session, render_template, redirect
from app.model import User, db, Compliant
from app.schema import isValidEmail 
from app.middleware import admin_required, login_required 

bp = Blueprint('admin', __name__)

@bp.route('/admin/complaints', methods=['GET'])
@admin_required
def admin_get_complaint():
    userID = session.get("user_id")
    user = User.query.filter(id = userID).first()
    departmentId = {'user_dep': user.department_id}
    complaints = Compliant.query.filter(department_id = departmentId)
    results = [
        {"id": c.id, "title": c.title, "description": c.description, "user_id": c.user_id}
        for c in complaints
    ]
    return jsonify(results), 200


@bp.route('/admin/complaints/<int:complaint_id>/status', methods=['PUT'])
@admin_required
def update_complaint(complaint_id):
    data = request.get_json() or request.form.to_dict()
    complaint = Compliant.query.filter(id = complaint_id)
    complaint.status = data.get('status',  complaint.status)
    db.session.commit()
    return jsonify({"message": "Complaint updated successfully", "status": complaint.status}), 200

@bp.route('/admin/complaints/<int:complaint_id>/respond', methods=['POST'])
@admin_required
def post_response_admin(complaint_id):
    data = request.get_json() or request.form.to_dict()
    complaint = Compliant.query.filter(id = complaint_id)
    complaint.admin_response = data.get('response',  complaint.admin_response)
    db.session.commit()
    return jsonify({"message": "Complaint updated successfully", "response": complaint.admin_response}), 200



