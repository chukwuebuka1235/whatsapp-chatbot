# To get the message sending , replace the def webhook in main.py with this code snippet 

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verification process
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        print(f"\nVerification attempt received:")
        print(f"Mode: {mode}")
        print(f"Token received: {token}")
        print(f"Expected token: {TOKEN}")
        
        if mode == "subscribe" and token == TOKEN:
            print("✅ Verification successful!")
            return make_response(challenge, 200)
        else:
            print("❌ Verification failed")
            return make_response("Verification failed", 403)
    
    elif request.method == "POST":
        try:
            data = request.get_json()
            print("\n📩 Incoming WhatsApp Message:", data)

            if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
                phone_number = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
                message_body = data["entry"][0]["changes"][0]["value"]["messages"][0].get("text", {}).get("body", "")

                from logic import handle_user_message
                handle_user_message(phone_number, message_body)

            return make_response("Message processed", 200)

        except Exception as e:
            print("❌ Error processing message:", e)
            return make_response("Error", 500)



#FOR BUTTONS
 "action": {
    "buttons": [
        {
            "type": "reply",
            "reply": {
                "id": "services_btn",
                "title": "View Services"
            }
        },
        {
            "type": "reply",
            "reply": {
                "id": "help_btn",
                "title": "Get Help"
            }
        }
    ]
 }





 # from flask import Flask, request, make_response
# import os
# from dotenv import load_dotenv
# import requests
# import secrets
# import string
# from pymongo import MongoClient
# from database import db_handler  # Import the database handler


# app = Flask(__name__)

# # Generate and load verification token
# def generate_verification_token(length=32):
#     alphabet = string.ascii_letters + string.digits
#     return ''.join(secrets.choice(alphabet) for _ in range(length))

# # Create .env file if it doesn't exist
# if not os.path.exists('.env'):
#     with open('.env', 'w') as f:
#         token = generate_verification_token()
#         f.write(f"TOKEN={token}\n")
#         f.write("ACCESS_TOKEN=your_facebook_access_token\n")
#         f.write("PHONE_NUMBER_ID=your_phone_number_id\n")
#     print("Generated new .env file with random token")

# # Load environment variables
# load_dotenv()
# TOKEN = os.getenv('TOKEN')
# ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
# PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

# # Verification endpoint
# @app.route("/webhook", methods=["GET", "POST"])
# def webhook():
#     if request.method == "GET":
#         # Verification process
#         mode = request.args.get("hub.mode")
#         token = request.args.get("hub.verify_token")
#         challenge = request.args.get("hub.challenge")
        
#         print(f"\nVerification attempt received:")
#         print(f"Mode: {mode}")
#         print(f"Token received: {token}")
#         print(f"Expected token: {TOKEN}")
        
#         if mode == "subscribe" and token == TOKEN:
#             print("✅ Verification successful!")
#             return make_response(challenge, 200)
#         else:
#             print("❌ Verification failed")
#             return make_response("Verification failed", 403)
    
#     elif request.method == "POST":
#         try:
#             data = request.get_json()
#             print("\n📩 Incoming WhatsApp Message:", data)

#             # Extract sender's phone number (if message received)
#             if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
#                 phone_number = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
#                 profile_name = data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
#                 print(f"\n📲 From: {phone_number} (Name: {profile_name})")

#                 send_whatsapp_template(
#                     to=phone_number,
#                     user_name=profile_name
#                 )

#             return make_response("Message processed", 200)
#         except Exception as e:
#             print("❌ Error processing message:", e)
#             return make_response("Error", 500)
        
# # Send WhatsApp Template Message
# def send_whatsapp_template(to, user_name):
#     url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "recipient_type": "individual",
#         "messaging_product": "whatsapp",
#         "to": to,
#         "type": "interactive",
#         "interactive": {
#             "type": "flow",
#             "header": {
#                 "type": "text",
#                 "text": "KadickMoni 2.0"
#             },
#             "body": {
# "text": f"""Hello {user_name}, welcome to Kadick Integrated Limited 🎉

# We offer a wide range of services:
# • Airtime and data recharge
# • Bill payments
# • Transfer and receive money into your virtual account
# • Secure card withdrawal transactions

# We're here to make your financial transactions fast, easy, and reliable. """
#             },
#             "footer": {
#                 "text": " Powered by Kadick Integrated Limited"
#             },
#            "action": {
#             "name": "flow",
#             "parameters": {
#                 "flow_message_version": "3",
#                 "flow_name": "Message templates_MARKETING_cef565b2-4",
#                 "flow_cta": "Get Started",
#             }
#            }
#         }
#         # "type": "template",
#         # "template": {
#         #     "name": template_name,
#         #     "language": { "code": language_code }
#         # }
  
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     print("\n📤 WhatsApp API Response:", response.json())
#     return response.json()

# @app.route("/test")
# def test():
#     return "Test endpoint is working!", 200

# if __name__ == "__main__":
#     print(f"\nYour verification token is: {TOKEN}")
#     print("Use this token in Meta Developer Dashboard")
#     print("Server running on http://localhost:5001")
#     app.run(port=5001, debug=True)

# # manual test
# # https://6d2febed90c6.ngrok-free.app/webhook?hub.mode=subscribe&hub.verify_token=YGwsVg9xjWvfJwXKFOkp4PoITI1xuxoJ&hub.challenge=12345