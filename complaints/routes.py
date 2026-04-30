from flask import Blueprint, request, jsonify
from models import Complaint
from app import db

complaints_bp = Blueprint('complaints', __name__)

# CREATE
@complaints_bp.route('/complaints', methods=['POST'])
@complaints_bp.route('/complaints', methods=['POST'])
def create_complaint():
    data = request.get_json()

    if not data.get('title') or not data.get('description') or not data.get('department_id') or not data.get('student_id'):
        return jsonify({"error": "All fields required"}), 400

    complaint = Complaint(
        title=data['title'],
        description=data['description'],
        department_id=data['department_id'],
        student_id=data['student_id']
    )

    db.session.add(complaint)
    db.session.commit()

    return jsonify({"message": "Complaint created"}), 201


# GET ALL
@complaints_bp.route('/complaints', methods=['GET'])
def get_complaints():
    # Get query parameters
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    student_id = request.args.get('student_id', type=int)

    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    # Start query
    query = Complaint.query.filter_by(student_id=student_id)

    # Filter by status if provided
    if status:
        query = query.filter_by(status=status)

    # Order by newest first
    query = query.order_by(Complaint.created_at.desc())

    # Pagination
    complaints = query.paginate(page=page, per_page=per_page)

    result = []
    for c in complaints.items:
        result.append({
            "id": c.id,
            "title": c.title,
            "status": c.status,
            "created_at": c.created_at
        })

    return jsonify({
        "total": complaints.total,
        "page": complaints.page,
        "pages": complaints.pages,
        "data": result
    }), 200


# GET ONE
@complaints_bp.route('/complaints/<int:id>', methods=['GET'])
def get_one(id):
    student_id = request.args.get('student_id', type=int)

    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    c = Complaint.query.get(id)

    if not c:
        return jsonify({"error": "Complaint not found"}), 404

    # Ownership check
    if c.student_id != student_id:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify({
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "status": c.status
    }), 200


# UPDATE
@complaints_bp.route('/complaints/<int:id>', methods=['PUT'])
def update_complaint(id):
    c = Complaint.query.get(id)

    if not c:
        return jsonify({"error": "Not found"}), 404

    if c.status != "Pending":
        return jsonify({"error": "Cannot edit"}), 403

    data = request.get_json()

    if 'title' in data:
        c.title = data['title']
    if 'description' in data:
        c.description = data['description']

    db.session.commit()

    return jsonify({"message": "Updated"}), 200


# DELETE
@complaints_bp.route('/complaints/<int:id>', methods=['DELETE'])
def delete_complaint(id):
    c = Complaint.query.get(id)

    if not c:
        return jsonify({"error": "Not found"}), 404

    if c.status != "Pending":
        return jsonify({"error": "Cannot delete"}), 403

    db.session.delete(c)
    db.session.commit()

    return jsonify({"message": "Deleted"}), 200