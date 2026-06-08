from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers.auth_controller import login_required
from models import db
from models.client import Client


client_bp = Blueprint("clients", __name__, url_prefix="/clientes")


def optional_email_from_form():
    email = request.form.get("email", "").strip()
    return email or None


@client_bp.route("/")
@login_required
def index():
    search = request.args.get("q", "").strip()
    query = Client.query
    if search:
        query = query.filter(Client.name.ilike(f"%{search}%"))
    clients = query.order_by(Client.name.asc()).all()
    return render_template("clients/index.html", clients=clients, search=search)


@client_bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        client = Client(
            name=request.form.get("name", "").strip(),
            phone=request.form.get("phone", "").strip(),
            email=optional_email_from_form(),
            notes=request.form.get("notes", "").strip(),
        )
        if not client.name or not client.phone:
            flash("Nome e telefone são obrigatórios.", "danger")
            return render_template("clients/form.html", client=client)

        db.session.add(client)
        db.session.commit()
        flash("Cliente cadastrado.", "success")
        return redirect(url_for("clients.index"))

    return render_template("clients/form.html", client=None)


@client_bp.route("/<int:client_id>/editar", methods=["GET", "POST"])
@login_required
def edit(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == "POST":
        client.name = request.form.get("name", "").strip()
        client.phone = request.form.get("phone", "").strip()
        client.email = optional_email_from_form()
        client.notes = request.form.get("notes", "").strip()

        if not client.name or not client.phone:
            flash("Nome e telefone são obrigatórios.", "danger")
            return render_template("clients/form.html", client=client)

        db.session.commit()
        flash("Cliente atualizado.", "success")
        return redirect(url_for("clients.index"))

    return render_template("clients/form.html", client=client)


@client_bp.route("/<int:client_id>/excluir", methods=["POST"])
@login_required
def delete(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash("Cliente excluído.", "success")
    return redirect(url_for("clients.index"))
