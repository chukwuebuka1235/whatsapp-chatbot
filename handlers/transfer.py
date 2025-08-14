def handle_transfer_money(phone_number, profile_name):
    # Start the transfer process with step 1
    return ask_transfer_amount(phone_number)

def ask_transfer_amount(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "💸 *Transfer Money*\n\nPlease enter the amount you want to transfer (in Naira):\nExample: _5000_"
        }
    }

def ask_select_bank(phone_number):
    # Nigerian banks list (top 5 for simplicity)
    banks = [
        {"id": "access_bank", "title": "Access Bank"},
        {"id": "gtb", "title": "GTBank"},
        {"id": "uba", "title": "UBA"},
        {"id": "zenith_bank", "title": "Zenith Bank"},
        {"id": "first_bank", "title": "First Bank"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "🏦 Select Bank"
            },
            "body": {
                "text": "Please select the recipient's bank:"
            },
            "action": {
                "button": "Bank List",
                "sections": [
                    {
                        "title": "Nigerian Banks",
                        "rows": banks
                    }
                ]
            }
        }
    }

def ask_account_number(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "🔢 Please enter the recipient's account number:"
        }
    }

def ask_remarks(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "📝 Please enter transaction remarks:"
        }
    }

def confirm_transfer(phone_number, amount, bank, account_number, remarks=""):
    return {
        "type": "text",
        "text": {
            "body": f"✅ *Transfer Confirmation*\n\n"
                    f"Amount: ₦{float(amount):,.2f}\n"
                    f"Bank: {bank}\n"
                    f"Account: {account_number}\n"
                    f"Remarks: {remarks}\n\n"
                    f"Reply 'CONFIRM' to complete the transfer."
        }
    }

def transfer_completed(phone_number, amount, bank, account_number):
    return {
        "type": "text",
        "text": {
            "body": f"✅ Transfer Successful!\n\n"
                    f"₦{float(amount):,.2f} has been sent to {account_number} at {bank}.\n"
                    f"Your new balance is ₦15,000.00"
        }
    }