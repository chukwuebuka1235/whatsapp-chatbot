def handle_check_balance(phone_number, profile_name):
    # In a real app, fetch from database
    account_number = "3298868791"
    balance = 15000.00
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": { 
                "text": f"🏦 Account Balance\n\n👤 Name: {profile_name}\n🔢 Account: {account_number}\n💰 Balance: ₦{balance:,.2f}"
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