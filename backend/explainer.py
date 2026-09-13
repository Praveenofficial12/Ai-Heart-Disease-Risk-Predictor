import os

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None

def generate_medical_explanation(result: dict) -> str:
    """
    Generate LLM-based medical explanation for heart disease risk
    """
    client = get_openai_client()
    if not client:
        return "LLM explanation unavailable (API key not configured)."

    # Prepare prompt for LLM
    prompt = f"""
You are a medical AI assistant.

Patient Heart Disease Risk Analysis:
- Risk Level: {result.get("risk_level")}
- Risk Score: {result.get("risk_score")}
- Indicators: {result.get("indicators")}
- Recommendations: {result.get("recommendations")}

Explain this result in:
1. Simple patient-friendly language
2. Medical reasoning
3. Lifestyle advice
4. Warning signs (if high risk)

Avoid diagnosis. Educational use only.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional medical explainer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=450
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM explanation failed: {str(e)}"

