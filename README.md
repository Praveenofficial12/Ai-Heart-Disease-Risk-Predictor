# ❤️ AI Heart Disease Risk Predictor

[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Backend](https://img.shields.io/badge/Backend-Flask-lightgrey)]()
[![Database](https://img.shields.io/badge/Database-MongoDB-green)]()
[![OCR](https://img.shields.io/badge/OCR-Tesseract-blue)]()

A comprehensive web application designed to assess cardiovascular risk using medical data, lifestyle indicators, and advanced AI-driven explanations. This tool empowers users to monitor their heart health through manual data entry or by uploading medical reports for automated analysis.

---

## 🚀 Key Features

- **Personalized Risk Assessment**: Rule-based engine that evaluates 15+ indicators including lipid profiles, lifestyle habits, and medical history.
- **Smart OCR Integration**: Upload a medical report (PDF/Image), and the system extracts key health metrics automatically.
- **AI-Powered Explanations**: Provides detailed clinical reasoning for the risk score, helping users understand "the why" behind their results.
- **Lifestyle Recommendations**: Actionable medical advice tailored to the user's risk level (Low, Moderate, High).
- **Comprehensive History Tracking**: Securely store and review past predictions to monitor progress over time.
- **Secure Authentication**: JWT-based login, password hashing (bcrypt), and profile management.
- **Interactive Dashboard**: Real-time stats and personalized health profile.

---

## 🛠️ Tech Stack

- **Frontend**: Clean, responsive UI built with HTML5, CSS3 (Modern Glassmorphism), and Vanilla JavaScript.
- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python) for robust API handling and logic.
- **Database**: [MongoDB Atlas](https://www.mongodb.com/atlas) for flexible and scalable data storage.
- **OCR Engine**: [Pytesseract](https://pypi.org/project/pytesseract/) for document text extraction.
- **Security**: Flask-JWT-Extended and Bcrypt for enterprise-grade security.
- **Notifications**: Flask-Mail for secure communication.

---

## 📋 System Architecture

1.  **User Layer**: Frontend interface for data entry and report uploads.
2.  **Processing Layer**:
    - **OCR Pipeline**: Processes PDF/Images to extract numeric health values.
    - **Predictor Engine**: Applies medical logic to calculate weighted risk scores.
    - **Explainer Module**: Generates human-readable clinical narratives.
3.  **Data Layer**: MongoDB collections for user profiles and prediction history.

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB Atlas Account (or local MongoDB)
- Tesseract OCR (installed on the host system)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Praveenofficial12/Ai-Heart-Disease-Risk-Predictor.git
   cd Ai-Heart-Disease-Risk-Predictor
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the `backend/` directory:
   ```env
   FLASK_SECRET_KEY=your_secret_key
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   ```

5. **Run the application**:
   ```bash
   python backend/app.py
   ```
   The app will be available at `http://localhost:5000`.

---

## 🌐 Deployment to Vercel

This project is pre-configured for seamless zero-config deployment on **Vercel**.

### Step 1: Push Changes to GitHub
Ensure all code changes, `vercel.json`, `api/index.py`, and `requirements.txt` are pushed to your GitHub repository:
```bash
git add .
git commit -m "Configure project for Vercel deployment"
git push origin main
```

### Step 2: Import Project in Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New > Project**.
2. Select your GitHub repository: `Praveenofficial12/Ai-Heart-Disease-Risk-Predictor`.
3. Framework Preset: **Other**.
4. Root Directory: `./` (leave default).

### Step 3: Configure Environment Variables in Vercel
Add the following key-value pairs in **Project Settings > Environment Variables**:
- `FLASK_SECRET_KEY` = your_secret_key
- `JWT_SECRET` = your_jwt_secret_key
- `MONGO_URI` = your_mongodb_atlas_connection_string
- `OPENAI_API_KEY` = (Optional) your_openai_api_key

### Step 4: Deploy!
Click **Deploy**. Vercel will automatically build the Python serverless function and host your website without errors.

---

## 🔍 How It Works

1.  **Login/Signup**: Create a secure account to track your heart health journey.
2.  **Choose Analysis Mode**:
    - **Manual**: Enter metrics like Blood Pressure, Cholesterol, Age, and Smoking status.
    - **Upload**: Drop a medical report to let the AI extract metrics automatically.
3.  **Receive Results**: Get a color-coded risk percentage, a detailed explanation, and a list of preventive actions.
4.  **Save & Review**: All results are saved to your dashboard for future reference.

---

## 🤝 Contribution

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📧 Contact

**Praveen Kumar K** - [praveen.kumar@example.com](mailto:praveen.kumar@example.com) - [LinkedIn](https://linkedin.com/in/praveenkumar)

Project Link: [https://github.com/Praveenofficial12/Ai-Heart-Disease-Risk-Predictor](https://github.com/Praveenofficial12/Ai-Heart-Disease-Risk-Predictor)

---
*Disclaimer: This tool is for educational purposes only and does not substitute professional medical advice.*