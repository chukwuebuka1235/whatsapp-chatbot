from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "whatsapp_bot")

# Connect to MongoDB
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Test connection
    db = client[DB_NAME]
    print("✅ Connected to MongoDB")
except ConnectionFailure as e:
    print(f"❌ MongoDB connection failed: {e}")
    raise

def save_user_data(phone_number: str, user_name: str, form_data: dict):
    """
    Save user data (phone, name, form data, timestamp) to MongoDB.
    """
    try:
        result = db.users.update_one(
            {"phone_number": phone_number},
            {"$set": {
                "phone_number": phone_number,
                "name": user_name,
                "timestamp": datetime.now(),
                **form_data  # Unpack all form data
            }},
            upsert=True
        )
        print(f"✅ User data saved/updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
        return True
    except Exception as e:
        print(f"❌ Error saving user data: {e}")
        return False

def check_user_exists(phone_number: str) -> bool:
    """
    Check if user exists in DB.
    """
    return db.users.count_documents({"phone_number": phone_number})