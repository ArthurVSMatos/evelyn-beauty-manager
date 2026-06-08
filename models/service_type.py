from datetime import datetime

from . import db


class ServiceType(db.Model):
    __tablename__ = "service_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    services = db.relationship("Service", back_populates="service_type")
