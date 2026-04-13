import pytesseract
from PIL import Image
import pdfplumber
import os

def extract_text(file_path):
    text = ""

    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

    return text
