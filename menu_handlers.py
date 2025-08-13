# menu_handlers.py

# menu_handlers.py (updated section)
def handle_menu_selection(selected_id, phone_number, profile_name):
    if selected_id == "check_balance":
        return handle_check_balance(phone_number, profile_name)
    elif selected_id == "transfer_money":
        return handle_transfer_money(phone_number, profile_name)
    elif selected_id == "buy_airtime":
        return handle_buy_airtime(phone_number, profile_name)
    elif selected_id == "buy_data":
        return handle_buy_data(phone_number, profile_name)  # Add this line
    elif selected_id == "pay_bills":  # Add this case
        return handle_pay_bills(phone_number, profile_name)
    elif selected_id == "transaction_history":
        return handle_transaction_history(phone_number, profile_name)
    else:
        return {"error": "Invalid selection"}


#HANDLE CHECK BALANCE
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


#HANDLE TRANSFER MONEY
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
            "body": "📝 Please enter transaction remarks (optional):"
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

#HANDLE BUY AIRTIME
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
    return {
        "type": "text",
        "text": {
            "body": f"✅ Airtime Purchase Successful!\n\n"
                    f"₦{float(amount):,.2f} airtime has been sent to {recharge_number} on {provider}.\n"
        }
    }

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



#HANDLE BUYING DATA 
def handle_buy_data(phone_number, profile_name):
    return ask_data_phone_number(phone_number)

def ask_data_phone_number(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "📱 *Buy Data*\n\nPlease enter your phone number:\nExample: _08012345678_"
        }
    }

def ask_data_provider(phone_number):
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
                "text": "Please select your network provider:"
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

def ask_data_duration(phone_number):
    durations = [
        {"id": "daily", "title": "Daily Plans"},
        {"id": "weekly", "title": "Weekly Plans"},
        {"id": "monthly", "title": "Monthly Plans"},
        {"id": "yearly", "title": "Yearly Plans"}
    ]
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "⏳ Select Plan Duration"
            },
            "body": {
                "text": "Choose the duration for your data plan:"
            },
            "action": {
                "button": "Duration",
                "sections": [
                    {
                        "title": "Data Plan Durations",
                        "rows": durations
                    }
                ]
            }
        }
    }

def ask_data_plan(phone_number, duration):
    plans = {
        "daily": [
            {"id": "daily_1", "title": "Daily 1GB - ₦200", "description": "1GB for 24 hours"},
            {"id": "daily_2", "title": "Daily 2.5GB - ₦500", "description": "2.5GB for 24 hours"}
        ],
        "weekly": [
            {"id": "weekly_1", "title": "Weekly 5GB - ₦1,000", "description": "5GB for 7 days"},
            {"id": "weekly_2", "title": "Weekly 10GB - ₦2,000", "description": "10GB for 7 days"}
        ],
        "monthly": [
            {"id": "monthly_1", "title": "Monthly 20GB - ₦5,000", "description": "20GB for 30 days"},
            {"id": "monthly_2", "title": "Monthly 50GB - ₦10,000", "description": "50GB for 30 days"}
        ],
        "yearly": [
            {"id": "yearly_1", "title": "Yearly 100GB - ₦20,000", "description": "100GB for 365 days"},
            {"id": "yearly_2", "title": "Yearly 200GB - ₦35,000", "description": "200GB for 365 days"}
        ]
    }
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "📊 Select Data Plan"
            },
            "body": {
                "text": f"Available {duration.capitalize()} Plans:"
            },
            "action": {
                "button": "Data Plans",
                "sections": [
                    {
                        "title": f"{duration.capitalize()} Data Plans",
                        "rows": plans.get(duration, [])
                    }
                ]
            }
        }
    }

def confirm_data(phone_number, recharge_number, provider, plan_title, plan_description):
    return {
        "type": "text",
        "text": {
            "body": f"✅ *Data Plan Confirmation*\n\n"
                    f"Number: {recharge_number}\n"
                    f"Network: {provider}\n"
                    f"Plan: {plan_title}\n"
                    f"Details: {plan_description}\n\n"
                    f"Reply 'CONFIRM' to purchase this data plan."
        }
    }

def data_completed(phone_number, recharge_number, provider, plan_title):
    return {
        "type": "text",
        "text": {
            "body": f"✅ Data Purchase Successful!\n\n"
                    f"Your {plan_title} has been activated for {recharge_number} on {provider}.\n"
                    f"Enjoy your data!"
        }
    }




# HANDLE PAY BILLS
def handle_pay_bills(phone_number, profile_name):
    bill_types = [
        {"id": "electricity", "title": "⚡ Electricity"},
        {"id": "cable_tv", "title": "📺 Cable TV"},
        {"id": "education", "title": "🎓 Education"},
        {"id": "betting", "title": "🎲 Betting"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "💳 Pay Bills"
            },
            "body": {
                "text": "Select the type of bill you want to pay:"
            },
            "action": {
                "button": "Bill Types",
                "sections": [
                    {
                        "title": "Bill Categories",
                        "rows": bill_types
                    }
                ]
            }
        }
    }

# ELECTRICITY BILL
def ask_electricity_provider(phone_number):
    providers = [
        {"id": "eedc", "title": "EEDC"},
        {"id": "eko", "title": "Eko Electricity"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "⚡ Electricity Provider"
            },
            "body": {
                "text": "Select your electricity provider:"
            },
            "action": {
                "button": "Providers",
                "sections": [
                    {
                        "title": "Electricity Providers",
                        "rows": providers
                    }
                ]
            }
        }
    }

def ask_payment_type(phone_number):
    types = [
        {"id": "prepaid", "title": "Prepaid"},
        {"id": "postpaid", "title": "Postpaid"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "🔌 Payment Type"
            },
            "body": {
                "text": "Select your payment type:"
            },
            "action": {
                "button": "Payment Type",
                "sections": [
                    {
                        "title": "Payment Types",
                        "rows": types
                    }
                ]
            }
        }
    }

def ask_meter_number(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "🔢 Please enter your meter number:"
        }
    }

def ask_electricity_amount(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "💵 Enter the amount you want to pay (in Naira):"
        }
    }

def confirm_electricity_payment(phone_number, provider, payment_type, meter_number, amount):
    return {
        "type": "text",
        "text": {
            "body": f"✅ *Electricity Payment Confirmation*\n\n"
                    f"Provider: {provider}\n"
                    f"Type: {payment_type}\n"
                    f"Meter: {meter_number}\n"
                    f"Amount: ₦{float(amount):,.2f}\n\n"
                    f"Reply 'CONFIRM' to complete the payment."
        }
    }

def electricity_payment_completed(phone_number, provider, meter_number, amount):
    return {
        "type": "text",
        "text": {
            "body": f"✅ Electricity Payment Successful!\n\n"
                    f"₦{float(amount):,.2f} has been paid for meter {meter_number} ({provider})."
        }
    }

# CABLE TV BILL
def ask_cable_provider(phone_number):
    providers = [
        {"id": "dstv", "title": "DSTV"},
        {"id": "gotv", "title": "GOTV"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "📺 Cable Provider"
            },
            "body": {
                "text": "Select your cable provider:"
            },
            "action": {
                "button": "Providers",
                "sections": [
                    {
                        "title": "Cable Providers",
                        "rows": providers
                    }
                ]
            }
        }
    }

def ask_cable_package(phone_number, provider):
    packages = {
        "dstv": [
            {"id": "dstv_box_office", "title": "Box Office - ₦5,000"},
            {"id": "dstv_compact", "title": "Compact - ₦10,000"},
            {"id": "dstv_premium", "title": "Premium - ₦20,000"}
        ],
        "gotv": [
            {"id": "gotv_lite", "title": "Lite - ₦2,000"},
            {"id": "gotv_max", "title": "Max - ₦5,000"},
            {"id": "gotv_supa", "title": "Supa - ₦8,000"}
        ]
    }
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": f"📦 {provider.upper()} Packages"
            },
            "body": {
                "text": f"Select your {provider} package:"
            },
            "action": {
                "button": "Packages",
                "sections": [
                    {
                        "title": f"{provider.upper()} Packages",
                        "rows": packages.get(provider, [])
                    }
                ]
            }
        }
    }

def ask_smartcard_number(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "🔢 Please enter your smartcard number:"
        }
    }

def confirm_cable_payment(phone_number, provider, package, smartcard_number):
    return {
        "type": "text",
        "text": {
            "body": f"✅ *Cable TV Payment Confirmation*\n\n"
                    f"Provider: {provider}\n"
                    f"Package: {package}\n"
                    f"Smartcard: {smartcard_number}\n\n"
                    f"Reply 'CONFIRM' to complete the payment."
        }
    }

def cable_payment_completed(phone_number, provider, package, smartcard_number):
    return {
        "type": "text",
        "text": {
            "body": f"✅ Cable TV Payment Successful!\n\n"
                    f"Your {package} package has been activated for smartcard {smartcard_number} ({provider})."
        }
    }

# EDUCATION BILL
def ask_education_biller(phone_number):
    billers = [
        {"id": "waec", "title": "WAEC"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "🎓 Education Biller"
            },
            "body": {
                "text": "Select the education biller:"
            },
            "action": {
                "button": "Billers",
                "sections": [
                    {
                        "title": "Education Billers",
                        "rows": billers
                    }
                ]
            }
        }
    }

def ask_waec_package(phone_number):
    packages = [
        {"id": "waec_1", "title": "1 PIN - ₦1,000"},
        {"id": "waec_2", "title": "2 PINs - ₦1,900"},
        {"id": "waec_5", "title": "5 PINs - ₦4,500"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "📝 WAEC Packages"
            },
            "body": {
                "text": "Select your WAEC package:"
            },
            "action": {
                "button": "Packages",
                "sections": [
                    {
                        "title": "WAEC Packages",
                        "rows": packages
                    }
                ]
            }
        }
    }

def ask_beneficiary_phone(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "📱 Enter beneficiary's phone number:"
        }
    }

def confirm_education_payment(phone_number, biller, package, beneficiary_phone):
    return {
        "type": "text",
        "text": {
            "body": f"✅ *Education Payment Confirmation*\n\n"
                    f"Biller: {biller}\n"
                    f"Package: {package}\n"
                    f"Beneficiary: {beneficiary_phone}\n\n"
                    f"Reply 'CONFIRM' to complete the payment."
        }
    }

def education_payment_completed(phone_number, biller, package, beneficiary_phone):
    return {
        "type": "text",
        "text": {
            "body": f"✅ Education Payment Successful!\n\n"
                    f"Your {package} has been sent to {beneficiary_phone}."
        }
    }

# BETTING BILL
def ask_betting_platform(phone_number):
    platforms = [
        {"id": "sporty", "title": "SportyBet"},
        {"id": "paripesa", "title": "Paripesa"},
        {"id": "bet9ja", "title": "Bet9ja"}
    ]
    
    return {
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "🎲 Betting Platform"
            },
            "body": {
                "text": "Select the betting platform:"
            },
            "action": {
                "button": "Platforms",
                "sections": [
                    {
                        "title": "Betting Platforms",
                        "rows": platforms
                    }
                ]
            }
        }
    }

def ask_customer_id(phone_number):
    return {
        "type": "text",
        "text": {
            "body": "🔢 Enter your customer ID:"
        }
    }

def confirm_betting_payment(phone_number, platform, customer_id):
    return {
        "type": "text",
        "text": {
            "body": f"✅ *Betting Payment Confirmation*\n\n"
                    f"Platform: {platform}\n"
                    f"Customer ID: {customer_id}\n\n"
                    f"Reply 'CONFIRM' to complete the payment."
        }
    }

def betting_payment_completed(phone_number, platform, customer_id):
    return {
        "type": "text",
        "text": {
            "body": f"✅ Betting Payment Successful!\n\n"
                    f"Your payment has been processed for customer ID {customer_id} on {platform}."
        }
    }