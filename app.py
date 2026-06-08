from decimal import Decimal
from pathlib import Path

from flask import Flask
from sqlalchemy import inspect, text

from config import Config
from controllers.appointment_controller import appointment_bp
from controllers.auth_controller import auth_bp
from controllers.client_controller import client_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.report_controller import report_bp
from controllers.service_controller import service_bp
from controllers.service_type_controller import service_type_bp
from models import db
from models.service import Service
from models.service_type import ServiceType
from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(service_type_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(report_bp)

    @app.template_filter("money")
    def money(value):
        return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @app.context_processor
    def inject_app_name():
        return {"app_name": app.config["APP_NAME"]}

    with app.app_context():
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
        db.create_all()
        ensure_schema_updates()
        seed_admin()
        seed_service_types()
        seed_services()
        assign_default_service_types()

    return app


def seed_admin():
    if User.query.filter_by(username=Config.ADMIN_USERNAME).first():
        return
    user = User(username=Config.ADMIN_USERNAME)
    user.set_password(Config.ADMIN_PASSWORD)
    db.session.add(user)
    db.session.commit()


def ensure_schema_updates():
    inspector = inspect(db.engine)
    if "services" not in inspector.get_table_names():
        return

    columns = [column["name"] for column in inspector.get_columns("services")]
    if "service_type_id" not in columns:
        db.session.execute(
            text(
                "ALTER TABLE services "
                "ADD COLUMN service_type_id INTEGER REFERENCES service_types(id)"
            )
        )
        db.session.commit()


def seed_service_types():
    default_types = [
        ("Sobrancelhas", "Design, modelagem e cuidados para sobrancelhas."),
        ("Cílios", "Aplicação e manutenção de cílios."),
        ("Depilação", "Serviços de depilação corporal."),
    ]

    for name, description in default_types:
        if not ServiceType.query.filter_by(name=name).first():
            db.session.add(ServiceType(name=name, description=description))
    db.session.commit()


def seed_services():
    service_types = {item.name: item for item in ServiceType.query.all()}
    default_services = [
        ("Design de sobrancelha", "Modelagem e finalização personalizada.", Decimal("45.00"), 45, "Sobrancelhas"),
        ("Extensão de cílios", "Aplicação completa com acabamento natural.", Decimal("140.00"), 120, "Cílios"),
        ("Manutenção de cílios", "Reposição e alinhamento dos fios.", Decimal("90.00"), 75, "Cílios"),
        ("Depilação de axila", "Depilação delicada e rápida.", Decimal("35.00"), 30, "Depilação"),
    ]

    for name, description, price, duration, type_name in default_services:
        if not Service.query.filter_by(name=name).first():
            db.session.add(
                Service(
                    name=name,
                    description=description,
                    service_type=service_types.get(type_name),
                    price=price,
                    duration_minutes=duration,
                    active=True,
                )
            )
    db.session.commit()


def assign_default_service_types():
    service_type_map = {
        "Design de sobrancelha": "Sobrancelhas",
        "Extensão de cílios": "Cílios",
        "Manutenção de cílios": "Cílios",
        "Depilação de axila": "Depilação",
    }
    service_types = {item.name: item for item in ServiceType.query.all()}

    for service_name, type_name in service_type_map.items():
        service = Service.query.filter_by(name=service_name).first()
        if service and not service.service_type_id and service_types.get(type_name):
            service.service_type = service_types[type_name]
    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
