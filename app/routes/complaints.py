from flask import Blueprint, request, jsonify, session
from app.model import Compliant, db, Department
# from app import db
from app.middleware import login_required, admin_required
from flask import render_template, redirect, url_for
from app.schema import isValidComplaint, isValidEmail

bp = Blueprint('complaints', __name__)


@bp.route('/complaints', methods=['POST'])
@login_required
def submit_complaint():
    data = request.form.to_dict()
    isValidComplaint(data)

    user = session.get("user_id")
    if user:
        complaint = Compliant(
            title=data["title"],
            description=data["description"],
            student_id= user,
            department_id = data["department"]
        )
        db.session.add(complaint)
        db.session.commit()
        print(complaint)
        return jsonify({"message": "Complaint submitted successfully"}), 201
    else: 
        redirect(url_for('get_login'), 201)

@bp.route('/complaints', methods=['GET'])
@login_required
def view_my_complaints():
    user_id = session.get('user_id')
    complaints = Compliant.query.filter_by(user_id=user_id).all()
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



# This should be in the admin route file
@bp.route('/complaints/all', methods=['GET'])
@admin_required
def view_all_complaints():
    complaints = Compliant.query.all()
    results = [
        {"id": c.id, "title": c.title, "description": c.description, "user_id": c.user_id}
        for c in complaints
    ]
    return jsonify(results), 200



@bp.route('/complaints/update/<int:complaint_id>', methods=['PUT'])
@admin_required
def update_complaint(complaint_id):
    data = request.get_json()
    complaint = Compliant.query.get_or_404(complaint_id)
    complaint.status = data.get('status', complaint.status)
    db.session.commit()
    return jsonify({"message": "Complaint updated successfully", "status": complaint.status}), 200



@bp.route('/complaints/mine/view')
@login_required
def student_dashboard():
    user_id = session.get('user_id')
    complaints = Compliant.query.filter_by(user_id=user_id).all()
    return render_template("student_dashboard.html", complaints=complaints)

@bp.route('/complaints/<int:complaint_id', methods=['DELETE'])
def delete(complaint_id):
    Compliant.query.filter(id=complaint_id).delete()
    db.session.commit()
    return jsonify({"Message": "Compliant Deleted Successfully"})