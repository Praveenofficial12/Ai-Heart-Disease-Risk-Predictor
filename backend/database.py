import os
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")

if not MONGO_URI:
    USERNAME = quote_plus("Praveen12")
    PASSWORD = quote_plus("Rocky@12")
    MONGO_URI = (
        f"mongodb+srv://{USERNAME}:{PASSWORD}"
        "@heartdiseaseriskpredict.uu2r5dy.mongodb.net/heart_disease_db"
        "?retryWrites=true&w=majority&tls=true&authSource=admin"
    )

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["heart_disease_db"]
users_col = db["users"]
history_col = db["history"]

try:
    client.server_info()
    print("✅ MongoDB Atlas Connected Successfully")
except Exception as e:
    print("⚠️ MongoDB Connection Warning:", e)

