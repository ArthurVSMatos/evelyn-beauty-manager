from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers.auth_controller import login_required
from models import db
from models.appointment import APPOINTMENT_STATUSES, PAYMENT_METHODS, PAYMENT_STATUSES, Appointment
from models.client import Client
from models.service import Service
from services.filters import appointment_query_from_args


appointment_bp = Blueprint("appointments", __name__, url_prefix="/agendamentos")


def _decimal_from_form(value):
    try:
        return Decimal((value or "0").replace(",", "."))
    except InvalidOperation:
        return Decimal("0")


def _form_options():
    return {
        "clients": Client.query.order_by(Client.name.asc()).all(),
        "services": Service.query.filter_by(active=True).order_by(Service.name.asc()).all(),
        "appointment_statuses": APPOINTMENT_STATUSES,
        "payment_statuses": PAYMENT_STATUSES,
        "payment_methods": PAYMENT_METHODS,
    }


@appointment_bp.route("/")
@login_required
def index():
    appointments = appointment_query_from_args(request.args).all()
    clients = Client.query.order_by(Client.name.asc()).all()
    services = Service.query.order_by(Service.name.asc()).all()
    return render_template(
        "appointments/index.html",
        appointments=appointments,
        clients=clients,
        services=services,
        appointment_statuses=APPOINTMENT_STATUSES,
        payment_statuses=PAYMENT_STATUSES,
        filters=request.args,
    )


@appointment_bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    appointment = None
    if request.method == "POST":
        appointment = _appointment_from_form()
        error = _validate_appointment(appointment)
        if error:
            flash(error, "danger")
            return render_template("appointments/form.html", appointment=appointment, **_form_options())

        db.session.add(appointment)
        db.session.commit()
        flash("Agendamento cadastrado.", "success")
        return redirect(url_for("appointments.index"))

    return render_template("appointments/form.html", appointment=appointment, **_form_options())


@appointment_bp.route("/<int:appointment_id>/editar", methods=["GET", "POST"])
@login_required
def edit(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if request.method == "POST":
        _update_appointment_from_form(appointment)
        error = _validate_appointment(appointment)
        if error:
            flash(error, "danger")
            return render_template("appointments/form.html", appointment=appointment, **_form_options())

        db.session.commit()
        flash("Agendamento atualizado.", "success")
        return redirect(url_for("appointments.index"))

    return render_template("appointments/form.html", appointment=appointment, **_form_options())


@appointment_bp.route("/<int:appointment_id>/excluir", methods=["POST"])
@login_required
def delete(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash("Agendamento excluído.", "success")
    return redirect(url_for("appointments.index"))


def _appointment_from_form():
    appointment = Appointment(amount=Decimal("0"))
    _update_appointment_from_form(appointment)
    return appointment


def _update_appointment_from_form(appointment):
    service_id = request.form.get("service_id")
    selected_service = Service.query.get(service_id) if service_id else None
    appointment.client_id = request.form.get("client_id")
    appointment.service_id = service_id
    appointment.scheduled_at = _scheduled_at_from_form(request.form.get("scheduled_at"))
    appointment.appointment_status = request.form.get("appointment_status") or "Agendado"
    appointment.payment_status = request.form.get("payment_status") or "Pendente"
    appointment.payment_method = request.form.get("payment_method") or "Pix"
    appointment.amount = _decimal_from_form(request.form.get("amount")) or (
        selected_service.price if selected_service else Decimal("0")
    )
    appointment.notes = request.form.get("notes", "").strip()


def _scheduled_at_from_form(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None


def _validate_appointment(appointment):
    if not appointment.client_id:
        return "Selecione uma cliente."
    if not appointment.service_id:
        return "Selecione um serviço."
    if not appointment.scheduled_at:
        return "Informe data e horário válidos."
    if appointment.appointment_status not in APPOINTMENT_STATUSES:
        return "Status do atendimento inválido."
    if appointment.payment_status not in PAYMENT_STATUSES:
        return "Status do pagamento inválido."
    if appointment.payment_method not in PAYMENT_METHODS:
        return "Forma de pagamento inválida."
    if appointment.amount < 0:
        return "O valor não pode ser negativo."
    return None
