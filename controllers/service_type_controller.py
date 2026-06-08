from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers.auth_controller import login_required
from models import db
from models.service_type import ServiceType


service_type_bp = Blueprint("service_types", __name__, url_prefix="/tipos-servicos")


@service_type_bp.route("/")
@login_required
def index():
    service_types = ServiceType.query.order_by(ServiceType.name.asc()).all()
    return render_template("service_types/index.html", service_types=service_types)


@service_type_bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        service_type = ServiceType(
            name=request.form.get("name", "").strip(),
            description=request.form.get("description", "").strip(),
        )
        if not service_type.name:
            flash("Nome do tipo de serviço é obrigatório.", "danger")
            return render_template("service_types/form.html", service_type=service_type)

        db.session.add(service_type)
        db.session.commit()
        flash("Tipo de serviço cadastrado.", "success")
        return redirect(url_for("service_types.index"))

    return render_template("service_types/form.html", service_type=None)


@service_type_bp.route("/<int:service_type_id>/editar", methods=["GET", "POST"])
@login_required
def edit(service_type_id):
    service_type = ServiceType.query.get_or_404(service_type_id)
    if request.method == "POST":
        service_type.name = request.form.get("name", "").strip()
        service_type.description = request.form.get("description", "").strip()

        if not service_type.name:
            flash("Nome do tipo de serviço é obrigatório.", "danger")
            return render_template("service_types/form.html", service_type=service_type)

        db.session.commit()
        flash("Tipo de serviço atualizado.", "success")
        return redirect(url_for("service_types.index"))

    return render_template("service_types/form.html", service_type=service_type)


@service_type_bp.route("/<int:service_type_id>/excluir", methods=["POST"])
@login_required
def delete(service_type_id):
    service_type = ServiceType.query.get_or_404(service_type_id)
    if service_type.services:
        flash("Este tipo possui serviços vinculados. Altere os serviços antes de excluir.", "warning")
        return redirect(url_for("service_types.index"))

    db.session.delete(service_type)
    db.session.commit()
    flash("Tipo de serviço excluído.", "success")
    return redirect(url_for("service_types.index"))
