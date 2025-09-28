from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 40
    for line in text.splitlines():
        c.drawString(40, y, line[:100])
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()

if __name__ == '__main__':
    md = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
    pdf = sys.argv[2] if len(sys.argv) > 2 else 'README.pdf'
    md_to_pdf(md, pdf)
