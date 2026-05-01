# This file involes the all validations involving incoming requests
"""
        This is the file that will hold all the functions involving the validation of data.
        The validation of incoming requests and everything involving data in the request and 
        response cycle.
"""

import re
from flask import jsonify

department_allowed = ['ICT', 'Cafeteria', 'Academics', 'Hostel']


def isValidEmail(email):
    pattern = "[a-zA-Z0-9]{1-20}[0-9]{5}@run.edu.ng"
    if re.fullmatch(pattern, email):
        return True
    else: 
        return False

def isValidComplaint(data):
    print(data)
    title = data['title']
    description = data['description']
    department = data['department']
    print(title)
    print(description)
    print(department)
    if title is None:
        return jsonify({"error": "1 Incomplete Complaint Request"}), 400
    if description is None:
        return jsonify({"error": "2 Incomplete Complaint Request"}), 400
    if department is None:
        return jsonify({"error": "3 Incomplete Complaint Request"}), 400
    if department not in department_allowed:
        return jsonify({"error": "4 Incomplete Complaint Request"}), 400
    else:
        return
