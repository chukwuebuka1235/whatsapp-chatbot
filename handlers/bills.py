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
    text = (
        f"✅ Electricity Payment Successful!\n\n"
        f"₦{float(amount):,.2f} has been paid for meter {meter_number} ({provider})."
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
    text = (
        f"✅ Cable TV Payment Successful!\n\n"
        f"Your {package} package has been activated for smartcard {smartcard_number} ({provider})."
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
    text = (
        f"✅ Education Payment Successful!\n\n"
        f"Your {package} has been sent to {beneficiary_phone}."
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
    text = (
        f"✅ Betting Payment Successful!\n\n"
        f"Your payment has been processed for customer ID {customer_id} on {platform}."
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
