import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from database import users_col, history_col
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "default_jwt_secret_key_heart_predictor_2026")

# ---------------- REGISTER ----------------
def register_user(email, password, phone):
    """
    Register new user
    """
    if users_col.find_one({"email": email}):
        return False

    users_col.insert_one({
        "email": email,
        "phone": phone,
        "password": generate_password_hash(password),
        "created_at": datetime.datetime.utcnow()
    })
    return True

# ---------------- LOGIN ----------------
def authenticate_user(email, password):
    """
    Authenticate user and return JWT token
    """
    user = users_col.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return None

    payload = {
        "user_id": str(user["_id"]),
        "email": email,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

# ---------------- VERIFY TOKEN ----------------
def verify_token(token):
    """
    Decode JWT token
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ---------------- UPDATE PASSWORD ----------------
def update_password(phone, new_password):
    """
    Update password using phone number (Forgot Password flow)
    """
    user = users_col.find_one({"phone": phone})
    if not user:
        return False

    users_col.update_one(
        {"phone": phone},
        {"$set": {
            "password": generate_password_hash(new_password),
            "updated_at": datetime.datetime.utcnow()
        }}
    )
    return True

# ---------------- USER HISTORY ----------------
def get_user_history(email):
    records = history_col.find({"email": email})
    return list(records)

# ---------------- DELETE HISTORY ----------------
def delete_user_history(email):
    result = history_col.delete_many({"email": email})
    return result.deleted_count
