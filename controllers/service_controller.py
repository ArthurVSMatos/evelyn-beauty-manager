from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers.auth_controller import login_required
from models import db
from models.service import Service
from models.service_type import ServiceType


service_bp = Blueprint("services", __name__, url_prefix="/servicos")


def _decimal_from_form(value):
    try:
        return Decimal((value or "0").replace(",", "."))
    except InvalidOperation:
        return Decimal("0")


def _service_type_id_from_form():
    return request.form.get("service_type_id") or None


def _service_form_context(service):
    return {
        "service": service,
        "service_types": ServiceType.query.order_by(ServiceType.name.asc()).all(),
    }


@service_bp.route("/")
@login_required
def index():
    services = Service.query.order_by(Service.name.asc()).all()
    return render_template("services/index.html", services=services)


@service_bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        service = Service(
            name=request.form.get("name", "").strip(),
            description=request.form.get("description", "").strip(),
            service_type_id=_service_type_id_from_form(),
            price=_decimal_from_form(request.form.get("price")),
            duration_minutes=int(request.form.get("duration_minutes") or 60),
            active=bool(request.form.get("active")),
        )
        if not service.name:
            flash("Nome do serviço é obrigatório.", "danger")
            return render_template("services/form.html", **_service_form_context(service))

        db.session.add(service)
        db.session.commit()
        flash("Serviço cadastrado.", "success")
        return redirect(url_for("services.index"))

    return render_template("services/form.html", **_service_form_context(None))


@service_bp.route("/<int:service_id>/editar", methods=["GET", "POST"])
@login_required
def edit(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == "POST":
        service.name = request.form.get("name", "").strip()
        service.description = request.form.get("description", "").strip()
        service.service_type_id = _service_type_id_from_form()
        service.price = _decimal_from_form(request.form.get("price"))
        service.duration_minutes = int(request.form.get("duration_minutes") or 60)
        service.active = bool(request.form.get("active"))

        if not service.name:
            flash("Nome do serviço é obrigatório.", "danger")
            return render_template("services/form.html", **_service_form_context(service))

        db.session.commit()
        flash("Serviço atualizado.", "success")
        return redirect(url_for("services.index"))

    return render_template("services/form.html", **_service_form_context(service))


@service_bp.route("/<int:service_id>/excluir", methods=["POST"])
@login_required
def delete(service_id):
    service = Service.query.get_or_404(service_id)
    if service.appointments:
        flash("Este serviço possui agendamentos. Desative em vez de excluir.", "warning")
        return redirect(url_for("services.index"))

    db.session.delete(service)
    db.session.commit()
    flash("Serviço excluído.", "success")
    return redirect(url_for("services.index"))
