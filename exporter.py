from fpdf import FPDF
import re

def clean_line(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def export_pdf(title, notes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, clean_line(title), ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", size=11)
    for line in notes.split("\n"):
        cleaned = clean_line(line)
        if cleaned.strip():
            pdf.multi_cell(0, 8, cleaned)
        else:
            pdf.ln(4)

    filename = "study_notes.pdf"
    pdf.output(filename)
    return filename