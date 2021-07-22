from django.shortcuts import render
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.platypus import Paragraph
from reportlab.platypus import PageBreak

def report_view(request):
    fileName = 'cistar_report.pdf'
    buffer = io.BytesIO()
    pagesize = (140 * mm, 216 * mm)  # width, height

    pdf = SimpleDocTemplate(buffer, pagesize=pagesize)
    sample_style_sheet = getSampleStyleSheet()
    paragraph = {}
    paragraph[0] = Paragraph("Report", sample_style_sheet['Heading1'])
    paragraph[1] = Paragraph("Calculation", sample_style_sheet['Heading2'])
    paragraph[2] = Paragraph(
    "Adiabatic temperature change: 86.667 °C",
    sample_style_sheet['BodyText']
    )
    paragraph[3] = Paragraph(
    "Calculated final temperature: 236.667 °C",
    sample_style_sheet['BodyText']
    )

    paragraph[4] = Paragraph("Alerts", sample_style_sheet['Heading2'])
    paragraph[5] = Paragraph("Reactant Alerts", sample_style_sheet['Heading3'])
    paragraph[6] = Paragraph(
    "Final temp exceeds reactant 1 boiling point",
    sample_style_sheet['BodyText']
    )
    paragraph[7] = Paragraph(
    "Final temp exceeds reactant 1 flash point",
    sample_style_sheet['BodyText']
    )
    paragraph[8] = Paragraph(
    "Final temp exceeds reactant 2 boiling point",
    sample_style_sheet['BodyText']
    )
    paragraph[9] = Paragraph(
    "Final temp exceeds reactant 2 flash point",
    sample_style_sheet['BodyText']
    )

    paragraph[10] = Paragraph("Product Alerts", sample_style_sheet['Heading3'])
    paragraph[11] = Paragraph(
    "Final temp exceeds product 1 boiling point",
    sample_style_sheet['BodyText']
    )
    paragraph[12] = Paragraph(
    "Final temp exceeds product 1 flash point",
    sample_style_sheet['BodyText']
    )
    paragraph[13] = Paragraph(
    "Final temp exceeds product 2 flash point",
    sample_style_sheet['BodyText']
    )

    paragraph[14] = Paragraph("Process Alerts", sample_style_sheet['Heading3'])
    paragraph[15] = Paragraph(
    "Final temp exceeds side reaction 1 temperature onset",
    sample_style_sheet['BodyText']
    )
    data = [
        ["A", "B", "C", "D"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"]
    ]
    table = Table(data)

    style = TableStyle(
        [
            ('BACKGROUND', (0,0), (3,0), colors.green),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER')
        ]
    )

    table.setStyle(style)
    elems = []
    for i in range(0, 16):
        elems.append(paragraph[i])

    elems.append(PageBreak())
    elems.append(table)

    pdf.build(elems)

    pdf_value = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cistar_report.pdf"'
    
    response.write(pdf_value)
    return response
