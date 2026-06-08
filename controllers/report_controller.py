from flask import Blueprint, Response, render_template, request

from controllers.auth_controller import login_required
from models.appointment import APPOINTMENT_STATUSES, PAYMENT_STATUSES
from models.client import Client
from models.service import Service
from services.filters import appointment_query_from_args
from services.pdf_service import generate_appointments_pdf


report_bp = Blueprint("reports", __name__, url_prefix="/relatorios")


@report_bp.route("/")
@login_required
def index():
    appointments = appointment_query_from_args(request.args).all()
    clients = Client.query.order_by(Client.name.asc()).all()
    services = Service.query.order_by(Service.name.asc()).all()
    return render_template(
        "reports/index.html",
        appointments=appointments,
        clients=clients,
        services=services,
        appointment_statuses=APPOINTMENT_STATUSES,
        payment_statuses=PAYMENT_STATUSES,
        filters=request.args,
    )


@report_bp.route("/pdf")
@login_required
def pdf():
    appointments = appointment_query_from_args(request.args).all()
    buffer = generate_appointments_pdf(appointments)
    return Response(
        buffer.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relatorio_atendimentos.pdf"},
    )
