#HANDLE TRANSACTION HISTORY
def handle_transaction_history(phone_number, profile_name):
    # Generate random transactions
    transactions = [
        {"date": "2024-05-15", "type": "Transfer", "amount": 5000.00, "recipient": "John Doe", "status": "Completed"},
        {"date": "2024-05-12", "type": "Airtime", "amount": 1000.00, "recipient": "0803****123", "status": "Success"},
        {"date": "2024-05-10", "type": "Deposit", "amount": 20000.00, "recipient": "", "status": "Completed"}
    ]
    
    history_text = "⏲ Recent Transactions:\n\n"
    for t in transactions:
        history_text += f"📅 {t['date']}\n"
        history_text += f"🔹 {t['type']}: ₦{t['amount']:,.2f}\n"
        if t['recipient']:
            history_text += f"👤 To: {t['recipient']}\n"
        history_text += f"✅ {t['status']}\n\n"
    
    return {
        "type": "text",
        "text": {
            "body": history_text
        }
    }
