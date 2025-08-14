import os
import secrets
import string
from dotenv import load_dotenv

# Generate and load verification token
def generate_verification_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Create .env file if it doesn't exist
def env_variables():
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            token = generate_verification_token()
            f.write(f"TOKEN={token}\n")
            f.write("ACCESS_TOKEN=your_facebook_access_token\n")
            f.write("PHONE_NUMBER_ID=your_phone_number_id\n")
            f.write("MONGODB_URI=mongodb://localhost:27017/\n")
            f.write("DB_NAME=kadick_db\n")
            f.write("WHATSAPP_TOKEN=your_facebook_access_token\n")
        print("Generated new .env file with random token")

    # Load environment variables
    load_dotenv()

    return {
        "TOKEN": os.getenv('TOKEN'),
        "ACCESS_TOKEN": os.getenv('ACCESS_TOKEN'),
        "PHONE_NUMBER_ID": os.getenv('PHONE_NUMBER_ID'),
        "MONGODB_URI": os.getenv('MONGODB_URI'),
        "DB_NAME": os.getenv('DB_NAME'),
        "WHATSAPP_TOKEN": os.getenv('WHATSAPP_TOKEN')
    }
