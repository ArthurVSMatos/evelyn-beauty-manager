from datetime import datetime

from . import db


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False, index=True)
    phone = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(140), nullable=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    appointments = db.relationship(
        "Appointment", back_populates="client", cascade="all, delete-orphan"
    )
