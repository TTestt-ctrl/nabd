from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from app import db
from app.models import Patient
from app.services import analytics

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        patient = Patient(
            full_name=request.form["full_name"],
            national_id=request.form["national_id"],
            phone=request.form["phone"],
            email=request.form["email"],
            date_of_birth=date.fromisoformat(request.form["date_of_birth"]),
            gender=request.form.get("gender"),
            allergies=request.form.get("allergies"),
            medications=request.form.get("medications"),
            medical_history=request.form.get("medical_history"),
        )
        patient.set_password(request.form["password"])
        db.session.add(patient)
        db.session.commit()

        analytics.track(patient.email, "Signed Up", {"gender": patient.gender})
        login_user(patient)
        return redirect(url_for("appointments.list_appointments"))

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        patient = Patient.query.filter_by(email=request.form["email"]).first()
        if patient and patient.check_password(request.form["password"]):
            login_user(patient)
            return redirect(url_for("appointments.list_appointments"))
        flash("Wrong email or password.")
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
