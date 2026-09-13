import os
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

class DummyCursor:
    def __init__(self, data=None):
        self.data = data or []
    def sort(self, *args, **kwargs):
        return self
    def __iter__(self):
        return iter(self.data)

class DummyResult:
    def __init__(self, count=0):
        self.deleted_count = count

class DummyCollection:
    def find_one(self, *args, **kwargs):
        return None
    def insert_one(self, *args, **kwargs):
        return None
    def update_one(self, *args, **kwargs):
        return None
    def find(self, *args, **kwargs):
        return DummyCursor([])
    def count_documents(self, *args, **kwargs):
        return 0
    def delete_many(self, *args, **kwargs):
        return DummyResult(0)

client = None
db = None
users_col = DummyCollection()
history_col = DummyCollection()

try:
    from pymongo import MongoClient
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=3000,
        connectTimeoutMS=3000
    )
    db = client["heart_disease_db"]
    users_col = db["users"]
    history_col = db["history"]
    print("✅ MongoDB Initialized")
except Exception as e:
    print("⚠️ MongoDB Initialization Warning:", e)
