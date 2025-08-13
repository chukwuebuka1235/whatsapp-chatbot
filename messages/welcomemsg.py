# messages/welcomemsg.py

def welcome_message(user_name: str, account_number: str, balance: float):
    balance_str = f"₦{balance:,.2f}"  # Format like ₦0.00
    
    text_message = (
        f"Account: ```{account_number}```\n"
        f"Balance: {balance_str}\n\n" 
    ) 

    return {
        "type": "interactive",
        "interactive": {
            "type": "list",  # dropdown menu
            "header":{
                "type": "text",
                "text": f"🏛Welcome, {user_name}"
            },
            "body": { 
                "text": text_message
            },
            "footer": {
                "text": "Select an option below 👇"
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
