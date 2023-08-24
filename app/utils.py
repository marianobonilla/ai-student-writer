from pdfminer.high_level import extract_text
from docx import Document

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_text_from_doc(doc_path):
    doc = Document(doc_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text