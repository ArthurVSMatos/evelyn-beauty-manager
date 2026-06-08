from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def br_money(value):
    return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generate_appointments_pdf(appointments, title="Relatorio de atendimentos"):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )
    styles = getSampleStyleSheet()
    elements = [
        Paragraph(title, styles["Title"]),
        Paragraph(datetime.now().strftime("Gerado em %d/%m/%Y as %H:%M"), styles["Normal"]),
        Spacer(1, 0.4 * cm),
    ]

    rows = [["Data", "Cliente", "Servico", "Valor", "Atendimento", "Pagamento"]]
    total = 0
    for item in appointments:
        total += float(item.amount or 0)
        rows.append(
            [
                item.scheduled_at.strftime("%d/%m/%Y %H:%M"),
                item.client.name,
                item.service.name,
                br_money(item.amount),
                item.appointment_status,
                item.payment_status,
            ]
        )

    if len(rows) == 1:
        rows.append(["-", "Nenhum registro encontrado", "-", "-", "-", "-"])

    table = Table(rows, colWidths=[3.1 * cm, 3.8 * cm, 3.8 * cm, 2.2 * cm, 2.8 * cm, 2.5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5f4b56")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8ccd2")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbf7f9")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 0.4 * cm))
    elements.append(Paragraph(f"Total listado: {br_money(total)}", styles["Heading3"]))

    document.build(elements)
    buffer.seek(0)
    return buffer
