from datetime import date, datetime, time

from flask import Blueprint, render_template
from sqlalchemy import extract, func

from controllers.auth_controller import login_required
from models import db
from models.appointment import Appointment


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    today = date.today()
    month_start = datetime(today.year, today.month, 1)
    today_start = datetime.combine(today, time.min)
    today_end = datetime.combine(today, time.max)

    todays_appointments = (
        Appointment.query.filter(Appointment.scheduled_at.between(today_start, today_end))
        .order_by(Appointment.scheduled_at.asc())
        .all()
    )
    pending_payments = Appointment.query.filter_by(payment_status="Pendente").count()
    reschedules = Appointment.query.filter_by(appointment_status="Remarcado").count()
    month_received = (
        db.session.query(func.coalesce(func.sum(Appointment.amount), 0))
        .filter(Appointment.payment_status == "Pago")
        .filter(Appointment.scheduled_at >= month_start)
        .filter(extract("year", Appointment.scheduled_at) == today.year)
        .scalar()
    )
    next_appointments = (
        Appointment.query.filter(Appointment.scheduled_at >= datetime.now())
        .order_by(Appointment.scheduled_at.asc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        todays_appointments=todays_appointments,
        pending_payments=pending_payments,
        month_received=month_received,
        reschedules=reschedules,
        next_appointments=next_appointments,
    )
