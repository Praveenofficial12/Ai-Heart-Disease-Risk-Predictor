import re

def parse_medical_data(text):
    data = {}

    age = re.search(r'Age[:\s]+(\d+)', text, re.I)
    cholesterol = re.search(r'Cholesterol[:\s]+(\d+)', text, re.I)
    bp = re.search(r'BP[:\s]+(\d+)/(\d+)', text, re.I)
    glucose = re.search(r'Glucose[:\s]+(\d+)', text, re.I)

    if age: data["age"] = int(age.group(1))
    if cholesterol: data["cholesterol"] = int(cholesterol.group(1))
    if bp:
        data["systolic_bp"] = int(bp.group(1))
    if glucose: data["glucose"] = int(glucose.group(1))

    return data
