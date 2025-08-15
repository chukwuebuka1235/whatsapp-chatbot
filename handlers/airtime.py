def handle_buy_airtime(phone_number, profile_name):
    return ask_airtime_phone_number(phone_number)

def ask_airtime_phone_number(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "📱 *Buy Airtime*\n\nPlease enter the phone number you want to recharge:\nExample: _08012345678_"
        }
    }

def ask_airtime_provider(phone_number):
    providers = [
        {"id": "mtn", "title": "MTN"},
        {"id": "airtel", "title": "Airtel"},
        {"id": "glo", "title": "Glo"},
        {"id": "9mobile", "title": "9Mobile"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "📶 Select Network"
            },
            "body": {
                "text": "Please select the recipient's network provider:"
            },
            "action": {
                "button": "Provider List",
                "sections": [
                    {
                        "title": "Network Providers",
                        "rows": providers
                    }
                ]
            }
        }
    }

def ask_airtime_amount(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "💵 Please enter the amount you want to recharge (in Naira):\nExample: _500_"
        }
    }

def confirm_airtime(phone_number, recharge_number, provider, amount):
    return {
        "type": "text",
        "text": {
            "body": f"✅ *Airtime Purchase Confirmation*\n\n"
                    f"Number: {recharge_number}\n"
                    f"Network: {provider}\n"
                    f"Amount: ₦{float(amount):,.2f}\n\n"
                    f"Reply 'CONFIRM' to complete the purchase."
        }
    }

def airtime_completed(phone_number, recharge_number, provider, amount):
    text = (
        f"✅ Airtime Purchase Successful!\n\n"
        f"₦{float(amount):,.2f} airtime has been sent to {recharge_number} on {provider}.\n"
    )

    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": text
            },
            "action": {
                "button": "📋 Menu Options",
                "sections": [
                    {
                        "title": "Available Actions",
                        "rows": [
                            {"id": "check_balance", "title": "💰 Check Balance"},
                            {"id": "transfer_money", "title": "💸 Transfer Money"},
                            {"id": "buy_airtime", "title": "📱 Buy Airtime"},
                            {"id": "buy_data", "title": "🌐 Buy Data"},
                            {"id": "pay_bills", "title": "💳 Pay Bills"},
                            {"id": "transaction_history", "title": "⏲ Transaction History"}
                        ]
                    }
                ]
            }
        }
    }