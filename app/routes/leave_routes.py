from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import db
from app.models import LeaveRequest

leave_bp = Blueprint("leave_bp", __name__)


# -----------------------------
# Create Leave Request
# -----------------------------
@leave_bp.route("/", methods=["POST"])
def create_leave():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    except Exception:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if end_date < start_date:
        return jsonify({"error": "End date cannot be before start date"}), 400

    leave = LeaveRequest(
        employee_name=data["employee_name"],
        start_date=start_date,
        end_date=end_date,
        reason=data["reason"],
        status="PENDING"
    )

    db.session.add(leave)
    db.session.commit()

    return jsonify({
        "id": leave.id,
        "status": leave.status
    }), 201


# -----------------------------
# Get All Leaves
# -----------------------------
@leave_bp.route("/all", methods=["GET"])
def get_all_leaves():
    leaves = LeaveRequest.query.all()

    result = []
    for leave in leaves:
        result.append({
            "id": leave.id,
            "employee_name": leave.employee_name,
            "start_date": leave.start_date.strftime("%Y-%m-%d"),
            "end_date": leave.end_date.strftime("%Y-%m-%d"),
            "reason": leave.reason,
            "status": leave.status
        })

    return jsonify(result), 200


# -----------------------------
# Approve Leave
# -----------------------------
@leave_bp.route("/<int:id>/approve", methods=["PUT"])
def approve_leave(id):
    leave = LeaveRequest.query.get_or_404(id)

    if leave.status != "PENDING":
        return jsonify({"error": "Leave already processed"}), 400

    leave.status = "APPROVED"
    db.session.commit()

    return jsonify({"message": "Leave approved"}), 200


# -----------------------------
# Reject Leave
# -----------------------------
@leave_bp.route("/<int:id>/reject", methods=["PUT"])
def reject_leave(id):
    leave = LeaveRequest.query.get_or_404(id)

    if leave.status != "PENDING":
        return jsonify({"error": "Leave already processed"}), 400

    leave.status = "REJECTED"
    db.session.commit()

    return jsonify({"message": "Leave rejected"}), 200