def handle_check_balance(phone_number, profile_name):
    # In a real app, fetch from database
    account_number = "3298868791"
    balance = 15000.00
    
    return {
        "type": "text",
        "text": {
            "body": f"🏦 Account Balance\n\n👤 Name: {profile_name}\n🔢 Account: {account_number}\n💰 Balance: ₦{balance:,.2f}"
        }
    }