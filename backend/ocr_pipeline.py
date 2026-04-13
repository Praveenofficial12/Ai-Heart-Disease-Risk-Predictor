import pytesseract
import re
from PIL import Image
from pdf2image import convert_from_path

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text
    else:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)

def parse_medical_report(text):
    def find(pattern, default=0):
        match = re.search(pattern, text, re.I)
        return match.group(1) if match else default

    return {
        "age": int(find(r"Age:\s*(\d+)")),
        "gender": 1 if "male" in text.lower() else 0,
        "smoking": 1 if "smoker" in text.lower() else 0,
        "alcohol": 1 if "frequent drinker" in text.lower() else 0,
        "cholesterol": int(find(r"Total Cholesterol:\s*(\d+)")),
        "triglycerides": int(find(r"Triglycerides:\s*(\d+)")),
        "ldl": int(find(r"LDL:\s*(\d+)")),
        "hdl": int(find(r"HDL:\s*(\d+)")),
        "systolic_bp": int(find(r"Systolic BP:\s*(\d+)")),
        "diastolic_bp": int(find(r"Diastolic BP:\s*(\d+)")),
        "diabetes": 1 if "diabetes" in text.lower() else 0,
        "hypertension": 1 if "hypertension" in text.lower() else 0,
        "stress": 1 if "high stress" in text.lower() else 0,
        "family_history": 1 if "father had heart disease" in text.lower() else 0
    }
