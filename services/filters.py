from datetime import datetime, time

from models.appointment import Appointment


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def appointment_query_from_args(args):
    query = Appointment.query

    date_value = parse_date(args.get("date"))
    if date_value:
        start = datetime.combine(date_value, time.min)
        end = datetime.combine(date_value, time.max)
        query = query.filter(Appointment.scheduled_at.between(start, end))

    if args.get("client_id"):
        query = query.filter(Appointment.client_id == args.get("client_id"))

    if args.get("service_id"):
        query = query.filter(Appointment.service_id == args.get("service_id"))

    if args.get("payment_status"):
        query = query.filter(Appointment.payment_status == args.get("payment_status"))

    if args.get("appointment_status"):
        query = query.filter(
            Appointment.appointment_status == args.get("appointment_status")
        )

    return query.order_by(Appointment.scheduled_at.desc())
