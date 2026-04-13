# predictor.py

def safe_int(value, default=0):
    """Safely convert input to int"""
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def clamp(val, min_val=0, max_val=100):
    return max(min(val, max_val), min_val)


def normalize_yes_no(value):
    if not value:
        return "No"
    return "Yes" if str(value).strip().lower() in ["yes", "y", "true", "1"] else "No"


def normalize_text(value):
    return str(value).strip().title() if value else ""


def stress_to_score(value):
    """Convert stress text or number into scale 0–10"""
    if isinstance(value, (int, float)):
        return clamp(int(value), 0, 10)

    text = str(value).lower()
    if "high" in text:
        return 8
    if "moderate" in text:
        return 5
    if "low" in text:
        return 2
    return 0


def calculate_risk(data):
    """
    Explainable rule-based heart disease risk analysis
    """

    score = 0.0
    indicators = {}

    # ---------------- DEMOGRAPHIC ----------------
    age = safe_int(data.get("age"))
    age_score = age * 0.25
    score += age_score
    indicators["Age"] = round(age_score, 2)

    gender = normalize_text(data.get("gender"))
    gender_score = 5 if gender == "Male" else 2
    score += gender_score
    indicators["Gender"] = gender_score

    # ---------------- LIFESTYLE ----------------
    smoking = normalize_yes_no(data.get("smoking"))
    alcohol = normalize_yes_no(data.get("alcohol"))

    smoking_score = 15 if smoking == "Yes" else 0
    alcohol_score = 8 if alcohol == "Yes" else 0

    physical = normalize_text(data.get("physical_activity"))
    physical_score = (
        12 if physical == "Low"
        else 6 if physical == "Moderate"
        else 0
    )

    score += smoking_score + alcohol_score + physical_score

    indicators.update({
        "Smoking": smoking_score,
        "Alcohol": alcohol_score,
        "Physical Activity": physical_score
    })

    # ---------------- MEDICAL CONDITIONS ----------------
    diabetes = normalize_yes_no(data.get("diabetes"))
    hypertension = normalize_yes_no(data.get("hypertension"))
    obesity = normalize_yes_no(data.get("obesity"))
    history = normalize_yes_no(data.get("heart_attack_history"))

    diabetes_score = 15 if diabetes == "Yes" else 0
    hypertension_score = 12 if hypertension == "Yes" else 0
    obesity_score = 10 if obesity == "Yes" else 0
    history_score = 25 if history == "Yes" else 0

    score += diabetes_score + hypertension_score + obesity_score + history_score

    indicators.update({
        "Diabetes": diabetes_score,
        "Hypertension": hypertension_score,
        "Obesity": obesity_score,
        "Previous Heart Attack": history_score
    })

    # ---------------- LIPID PROFILE ----------------
    cholesterol = safe_int(data.get("cholesterol"))
    triglycerides = safe_int(
        data.get("triglycerides") or data.get("triglyceride")
    )
    ldl = safe_int(data.get("ldl"))
    hdl = safe_int(data.get("hdl"))

    cholesterol_score = cholesterol * 0.04
    triglyceride_score = triglycerides * 0.03
    ldl_score = ldl * 0.05
    hdl_score = -hdl * 0.04  # Protective factor

    score += cholesterol_score + triglyceride_score + ldl_score + hdl_score

    indicators.update({
        "Cholesterol": round(cholesterol_score, 2),
        "Triglycerides": round(triglyceride_score, 2),
        "LDL": round(ldl_score, 2),
        "HDL (Protective)": round(hdl_score, 2)
    })

    # ---------------- BLOOD PRESSURE ----------------
    systolic = safe_int(data.get("systolic_bp"))
    diastolic = safe_int(data.get("diastolic_bp"))

    systolic_score = systolic * 0.05
    diastolic_score = diastolic * 0.04

    score += systolic_score + diastolic_score

    indicators.update({
        "Systolic BP": round(systolic_score, 2),
        "Diastolic BP": round(diastolic_score, 2)
    })

    # ---------------- STRESS & ENVIRONMENT ----------------
    stress_value = stress_to_score(data.get("stress"))
    stress_score = stress_value * 2
    score += stress_score
    indicators["Stress"] = stress_score

    family = normalize_yes_no(data.get("family_history"))
    family_score = 10 if family == "Yes" else 0
    score += family_score
    indicators["Family History"] = family_score

    healthcare = normalize_text(data.get("healthcare_access"))
    healthcare_score = (
        8 if healthcare == "Poor"
        else 4 if healthcare == "Moderate"
        else 0
    )

    score += healthcare_score
    indicators["Healthcare Access"] = healthcare_score

    # ---------------- FINAL SCORING ----------------
    MAX_SCORE = 200
    risk_percent = clamp((score / MAX_SCORE) * 100)

    if risk_percent < 30:
        risk_level = "Low Risk"
        color = "green"
    elif risk_percent < 65:
        risk_level = "Moderate Risk"
        color = "orange"
    else:
        risk_level = "High Risk"
        color = "red"

    # ---------------- EXPLANATION ----------------
    explanation = (
        f"Based on the provided medical and lifestyle information, the individual "
        f"is classified under the {risk_level} category. The assessment considers "
        f"age, habits, medical conditions, cholesterol levels, blood pressure, "
        f"stress levels, and family history. Preventive actions can help reduce "
        f"future cardiovascular risk."
    )

    # ---------------- RECOMMENDATIONS ----------------
    recommendations = {
        "Low Risk": [
            "Maintain a balanced diet",
            "Exercise at least 150 minutes per week",
            "Avoid smoking and excess alcohol",
            "Annual preventive health checkups"
        ],
        "Moderate Risk": [
            "Reduce salt, sugar, and saturated fats",
            "Engage in regular physical activity",
            "Manage stress through yoga or meditation",
            "Monitor BP and cholesterol regularly"
        ],
        "High Risk": [
            "Consult a cardiologist immediately",
            "Follow a strict heart-healthy diet",
            "Quit smoking and alcohol completely",
            "Take prescribed medications consistently",
            "Frequent cardiac monitoring"
        ]
    }[risk_level]

    # ---------------- RETURN ----------------
    return {
        "risk_score": round(score, 2),
        "risk_percent": round(risk_percent, 1),
        "risk_level": risk_level,
        "risk_color": color,
        "indicators": indicators,
        "explanation": explanation,
        "recommendations": recommendations
    }
