from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Appointment
from app.services import analytics, payments, storage

bp = Blueprint("appointments", __name__, url_prefix="/appointments")


@bp.route("/", methods=["GET"])
@login_required
def list_appointments():
    appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    return render_template("appointments/list.html", appointments=appointments)


@bp.route("/book", methods=["POST"])
@login_required
def book():
    appointment = Appointment(
        patient_id=current_user.id,
        clinic=request.form["clinic"],
        doctor_name=request.form["doctor_name"],
        reason=request.form.get("reason"),
        scheduled_at=datetime.fromisoformat(request.form["scheduled_at"]),
    )

    payment = payments.charge(
        amount_halalas=int(request.form["amount"]),
        description=f"Nabd appointment at {appointment.clinic}",
        source_token=request.form["payment_token"],
    )
    appointment.payment_id = payment["id"]

    report = request.files.get("medical_report")
    if report:
        appointment.report_key = storage.upload_report(current_user.id, report)

    db.session.add(appointment)
    db.session.commit()

    analytics.track(
        current_user.email,
        "Appointment Booked",
        {"clinic": appointment.clinic, "reason": appointment.reason},
    )
    return redirect(url_for("appointments.list_appointments"))


@bp.route("/<int:appointment_id>/cancel", methods=["POST"])
@login_required
def cancel(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = "cancelled"
    db.session.commit()
    return redirect(url_for("appointments.list_appointments"))
