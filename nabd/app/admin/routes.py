from flask import Blueprint, jsonify

from app import db
from app.models import Appointment, Patient

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/patients", methods=["GET"])
def patients():
    rows = Patient.query.order_by(Patient.created_at.desc()).all()
    return jsonify(
        [
            {
                "id": p.id,
                "full_name": p.full_name,
                "national_id": p.national_id,
                "phone": p.phone,
                "email": p.email,
                "allergies": p.allergies,
                "medications": p.medications,
            }
            for p in rows
        ]
    )


@bp.route("/patients/<int:patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    Appointment.query.filter_by(patient_id=patient.id).delete()
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"deleted": patient_id})
