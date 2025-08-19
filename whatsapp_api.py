import requests
from config import env_variables

config = env_variables()

def send_whatsapp_message(phone_number, text):
    url = f"https://graph.facebook.com/v18.0/{config['PHONE_NUMBER_ID']}/messages"
    headers = {
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"📤 WhatsApp message status: {response.status_code} | {response.text}")

def send_whatsapp_interactive(phone_number, interactive_payload):
    url = f"https://graph.facebook.com/v18.0/{config['PHONE_NUMBER_ID']}/messages"
    headers = {
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        **interactive_payload
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"📤 WhatsApp interactive message status: {response.status_code} | {response.text}")

def send_whatsapp_template(to, user_name):
    url = f"https://graph.facebook.com/v18.0/{config['PHONE_NUMBER_ID']}/messages"
    headers = {
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient_type": "individual",
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "flow",
            "header": {
                "type": "text",
                "text": "KadickMoni 2.0"
            },
            "body": {
                "text": f"""Hello {user_name}, welcome to Kadick Integrated Limited 🎉

We offer a wide range of services:
• Airtime and data recharge
• Bill payments
• Transfer and receive money into your virtual account
• Secure card withdrawal transactions

We're here to make your financial transactions fast, easy, and reliable. """
            },
            "footer": {
                "text": " Powered by Kadick Integrated Limited"
            },
            "action": {
                "name": "flow",
                "parameters": {
                    "flow_message_version": "3",
                    "flow_name": "Message templates_MARKETING_cef565b2-4",
                    "flow_cta": "Get Started",
                }
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    print("\n📤 WhatsApp API Response:", response.json())
    return response.json()