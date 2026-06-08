from datetime import datetime

from . import db


APPOINTMENT_STATUSES = ("Agendado", "Realizado", "Remarcado", "Cancelado")
PAYMENT_STATUSES = ("Pago", "Pendente")
PAYMENT_METHODS = ("Pix", "Dinheiro", "Cartao", "Outro")


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False, index=True)
    appointment_status = db.Column(
        db.String(20), nullable=False, default="Agendado", index=True
    )
    payment_status = db.Column(
        db.String(20), nullable=False, default="Pendente", index=True
    )
    payment_method = db.Column(db.String(20), nullable=False, default="Pix")
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    client = db.relationship("Client", back_populates="appointments")
    service = db.relationship("Service", back_populates="appointments")
