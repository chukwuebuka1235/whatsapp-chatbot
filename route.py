
from flask import Flask, request, make_response
from config import env_variables
import json
from whatsapp.wapp import process_message

app = Flask(__name__)
config = env_variables()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return verify_webhook()
    elif request.method == "POST":
        return handle_incoming_message()


def verify_webhook():
    """
    Verify the webhook with Facebook.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"\nVerification attempt received: Mode={mode}, Token={token}")

    if mode == "subscribe" and token == config['TOKEN']:
        print("✅ Verification successful!")
        return make_response(challenge, 200)
    else:
        print("❌ Verification failed")
        return make_response("Verification failed", 403)

def handle_incoming_message():
    try:
        data = request.get_json()
        print("\n📩 Incoming WhatsApp Message:", json.dumps(data, indent=2))  # Better logging

        if process_message(data):
            return make_response("Message processed", 200)
        else:
            return make_response("Message not processed", 400)
    except Exception as e:
        print("❌ Error processing message:", e)
        return make_response("Error", 500)
    
 