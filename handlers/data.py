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
