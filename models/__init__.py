from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from .appointment import Appointment  # noqa: E402,F401
from .client import Client  # noqa: E402,F401
from .service import Service  # noqa: E402,F401
from .service_type import ServiceType  # noqa: E402,F401
from .user import User  # noqa: E402,F401
