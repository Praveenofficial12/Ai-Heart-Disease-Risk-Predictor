from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os, time

def generate_pdf(result, filename):
    path = f"../frontend/static/reports/{filename}"

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>Hospital Medical Report</b>", styles["Title"]))
    content.append(Paragraph(f"Date: {time.strftime('%d-%m-%Y')}", styles["Normal"]))

    content.append(Paragraph("<b>Risk Summary</b>", styles["Heading2"]))
    content.append(Paragraph(f"Risk Level: {result['risk_level']}", styles["Normal"]))
    content.append(Paragraph(f"Risk Percentage: {result['risk_percent']}%", styles["Normal"]))
    content.append(Paragraph(f"Risk Score: {result['risk_score']}", styles["Normal"]))

    content.append(Paragraph("<b>Medical Explanation</b>", styles["Heading2"]))
    content.append(Paragraph(result["explanation"], styles["Normal"]))

    content.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))
    for rec in result["recommendations"]:
        content.append(Paragraph(f"- {rec}", styles["Normal"]))

    doc.build(content)
    return path
