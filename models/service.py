from decimal import Decimal

from . import db


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text)
    service_type_id = db.Column(db.Integer, db.ForeignKey("service_types.id"), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    duration_minutes = db.Column(db.Integer, nullable=False, default=60)
    active = db.Column(db.Boolean, nullable=False, default=True)

    service_type = db.relationship("ServiceType", back_populates="services")
    appointments = db.relationship("Appointment", back_populates="service")
