import os
from dotenv import load_dotenv
from flask import Flask, request, make_response
import requests
import json
from database import save_user_data , check_user_exists
from messages.welcomemsg import welcome_message
from handlers import handle_menu_selection
from config import env_variables

from handlers.transfer import (
    ask_transfer_amount, 
    ask_select_bank,
    ask_account_number,
    ask_remarks,
    confirm_transfer,
    transfer_completed
)
from handlers.airtime import (
    ask_airtime_phone_number,
    ask_airtime_provider,
    ask_airtime_amount,
    confirm_airtime,
    airtime_completed
)
from handlers.data import (
    ask_data_phone_number,
    ask_data_provider,
    ask_data_duration,
    ask_data_plan,
    confirm_data,
    data_completed
)
from handlers.bills import (
    handle_pay_bills,
    ask_electricity_provider,
    ask_payment_type,
    ask_meter_number,
    ask_electricity_amount,
    confirm_electricity_payment,
    electricity_payment_completed,
    ask_cable_provider,
    ask_cable_package,
    ask_smartcard_number,
    confirm_cable_payment,
    cable_payment_completed,
    ask_education_biller,
    ask_waec_package,
    ask_beneficiary_phone,
    confirm_education_payment,
    education_payment_completed,
    ask_betting_platform,
    ask_customer_id,
    confirm_betting_payment,
    betting_payment_completed
)

app = Flask(__name__)
config = env_variables()

def process_message(data):
        try:
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if messages:
                message = messages[0]
                phone_number = message.get("from")
                profile_name = value.get("contacts", [{}])[0].get("profile", {}).get("name", "User")

                # --- Airtime purchase process handling ---
                if phone_number in user_airtime_state:
                    state = user_airtime_state[phone_number]

                    if state["step"] == "phone":
                        if message.get('type') == 'text':
                            recharge_number = message['text']['body']
                            if len(recharge_number) >= 10 and recharge_number.isdigit():
                                user_airtime_state[phone_number] = {
                                    "step": "provider",
                                    "recharge_number": recharge_number
                                }
                                response = ask_airtime_provider(phone_number)
                                send_whatsapp_interactive(phone_number, response)
                            else:
                                send_whatsapp_message(phone_number, "❌ Invalid phone number. Please enter a valid 10 or 11 digit number.")
                        return make_response("Airtime step handled", 200)

                    elif state["step"] == "provider":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            provider_id = message['interactive']['list_reply']['id']
                            provider_title = next(
                                (p['title'] for p in [
                                    {"id": "mtn", "title": "MTN"},
                                    {"id": "airtel", "title": "Airtel"},
                                    {"id": "glo", "title": "Glo"},
                                    {"id": "9mobile", "title": "9Mobile"}
                                ] if p['id'] == provider_id),
                                "Unknown Provider"
                            )
                            user_airtime_state[phone_number] = {
                                "step": "amount",
                                "recharge_number": state["recharge_number"],
                                "provider": provider_title
                            }
                            response = ask_airtime_amount(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Airtime step handled", 200)

                    elif state["step"] == "amount":
                        if message.get('type') == 'text':
                            amount = message['text']['body']
                            try:
                                float(amount)
                                user_airtime_state[phone_number] = {
                                    "step": "confirm",
                                    "recharge_number": state["recharge_number"],
                                    "provider": state["provider"],
                                    "amount": amount
                                }
                                response = confirm_airtime(
                                    phone_number,
                                    state["recharge_number"],
                                    state["provider"],
                                    amount
                                )
                                send_whatsapp_message(phone_number, response["text"]["body"])
                            except ValueError:
                                send_whatsapp_message(phone_number, "❌ Invalid amount. Please enter a valid number.")
                        return make_response("Airtime step handled", 200)

                    elif state["step"] == "confirm":
                        if message.get('type') == 'text' and message['text']['body'].strip().lower() == 'confirm':
                            response = airtime_completed(
                                phone_number,
                                state["recharge_number"],
                                state["provider"],
                                state["amount"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            del user_airtime_state[phone_number]
                        else:
                            send_whatsapp_message(phone_number, "❌ Purchase cancelled. Type 'CONFIRM' to complete the airtime purchase.")
                        return make_response("Airtime step handled", 200)

                # --- Transfer process handling ---
                if phone_number in user_transfer_state:
                    state = user_transfer_state[phone_number]

                    if state["step"] == "amount":
                        if message.get('type') == 'text':
                            amount = message['text']['body']
                            try:
                                float(amount)
                                user_transfer_state[phone_number] = {
                                    "step": "bank",
                                    "amount": amount
                                }
                                response = ask_select_bank(phone_number)
                                send_whatsapp_interactive(phone_number, response)
                            except ValueError:
                                send_whatsapp_message(phone_number, "❌ Invalid amount. Please enter a valid number.")
                        return make_response("Transfer step handled", 200)

                    elif state["step"] == "bank":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            bank_id = message['interactive']['list_reply']['id']
                            bank_title = next(
                                (bank['title'] for bank in [
                                    {"id": "access_bank", "title": "Access Bank"},
                                    {"id": "gtb", "title": "GTBank"},
                                    {"id": "uba", "title": "UBA"},
                                    {"id": "zenith_bank", "title": "Zenith Bank"},
                                    {"id": "first_bank", "title": "First Bank"}
                                ] if bank['id'] == bank_id),
                                "Unknown Bank"
                            )
                            user_transfer_state[phone_number] = {
                                "step": "account",
                                "amount": state["amount"],
                                "bank": bank_title
                            }
                            response = ask_account_number(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Transfer step handled", 200)

                    elif state["step"] == "account":
                        if message.get('type') == 'text':
                            account_number = message['text']['body']
                            if account_number.isdigit() and len(account_number) >= 10:
                                user_transfer_state[phone_number] = {
                                    "step": "remarks",
                                    "amount": state["amount"],
                                    "bank": state["bank"],
                                    "account_number": account_number
                                }
                                response = ask_remarks(phone_number)
                                send_whatsapp_message(phone_number, response["text"]["body"])
                            else:
                                send_whatsapp_message(phone_number, "❌ Invalid account number. Please enter a valid account number.")
                        return make_response("Transfer step handled", 200)

                    elif state["step"] == "remarks":
                        if message.get('type') == 'text':
                            remarks = message['text']['body']
                            user_transfer_state[phone_number] = {
                                "step": "confirm",
                                "amount": state["amount"],
                                "bank": state["bank"],
                                "account_number": state["account_number"],
                                "remarks": remarks
                            }
                            response = confirm_transfer(
                                phone_number,
                                state["amount"],
                                state["bank"],
                                state["account_number"],
                                remarks
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Transfer step handled", 200)

                    elif state["step"] == "confirm":
                        if message.get('type') == 'text' and message['text']['body'].strip().lower() == 'confirm':
                            response = transfer_completed(
                                phone_number,
                                state["amount"],
                                state["bank"],
                                state["account_number"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            del user_transfer_state[phone_number]
                        else:
                            send_whatsapp_message(phone_number, "❌ Transfer cancelled. Type 'CONFIRM' to complete the transfer.")
                        return make_response("Transfer step handled", 200)

                # --- Data purchase process handling ---
                if phone_number in user_data_state:
                    state = user_data_state[phone_number]

                    if state["step"] == "phone":
                        if message.get('type') == 'text':
                            recharge_number = message['text']['body']
                            if len(recharge_number) >= 10 and recharge_number.isdigit():
                                user_data_state[phone_number] = {
                                    "step": "provider",
                                    "recharge_number": recharge_number
                                }
                                response = ask_data_provider(phone_number)
                                send_whatsapp_interactive(phone_number, response)
                            else:
                                send_whatsapp_message(phone_number, "❌ Invalid phone number. Please enter a valid 10 or 11 digit number.")
                        return make_response("Data step handled", 200)

                    elif state["step"] == "provider":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            provider_id = message['interactive']['list_reply']['id']
                            provider_title = next(
                                (p['title'] for p in [
                                    {"id": "mtn", "title": "MTN"},
                                    {"id": "airtel", "title": "Airtel"},
                                    {"id": "glo", "title": "Glo"},
                                    {"id": "9mobile", "title": "9Mobile"}
                                ] if p['id'] == provider_id),
                                "Unknown Provider"
                            )
                            user_data_state[phone_number] = {
                                "step": "duration",
                                "recharge_number": state["recharge_number"],
                                "provider": provider_title
                            }
                            response = ask_data_duration(phone_number)
                            send_whatsapp_interactive(phone_number, response)
                        return make_response("Data step handled", 200)

                    elif state["step"] == "duration":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            duration = message['interactive']['list_reply']['id']
                            user_data_state[phone_number] = {
                                "step": "plan",
                                "recharge_number": state["recharge_number"],
                                "provider": state["provider"],
                                "duration": duration
                            }
                            response = ask_data_plan(phone_number, duration)
                            send_whatsapp_interactive(phone_number, response)
                        return make_response("Data step handled", 200)

                    elif state["step"] == "plan":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            plan_id = message['interactive']['list_reply']['id']
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
                            selected_plan = next(
                                (p for p in plans.get(state["duration"], []) if p['id'] == plan_id),
                                {"title": "Unknown Plan", "description": ""}
                            )
                            user_data_state[phone_number] = {
                                "step": "confirm",
                                "recharge_number": state["recharge_number"],
                                "provider": state["provider"],
                                "plan_title": selected_plan["title"],
                                "plan_description": selected_plan["description"]
                            }
                            response = confirm_data(
                                phone_number,
                                state["recharge_number"],
                                state["provider"],
                                selected_plan["title"],
                                selected_plan["description"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Data step handled", 200)

                    elif state["step"] == "confirm":
                        if message.get('type') == 'text' and message['text']['body'].lower() == 'confirm':
                            response = data_completed(
                                phone_number,
                                state["recharge_number"],
                                state["provider"],
                                state["plan_title"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            del user_data_state[phone_number]
                        else:
                            send_whatsapp_message(phone_number, "❌ Purchase cancelled. Type 'CONFIRM' to complete the data purchase.")
                        return make_response("Data step handled", 200)

                # --- Bill payment handling ---
                # Electricity bill
                if phone_number in user_electricity_state:
                    state = user_electricity_state[phone_number]
                    if state["step"] == "provider":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            provider_id = message['interactive']['list_reply']['id']
                            provider_title = next(
                                (p['title'] for p in [
                                    {"id": "eedc", "title": "EEDC"},
                                    {"id": "eko", "title": "Eko Electricity"}
                                ] if p['id'] == provider_id),
                                "Unknown Provider"
                            )
                            user_electricity_state[phone_number] = {
                                "step": "payment_type",
                                "provider": provider_title
                            }
                            response = ask_payment_type(phone_number)
                            send_whatsapp_interactive(phone_number, response)
                        return make_response("Electricity step handled", 200)
                    elif state["step"] == "payment_type":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            type_id = message['interactive']['list_reply']['id']
                            type_title = next(
                                (t['title'] for t in [
                                    {"id": "prepaid", "title": "Prepaid"},
                                    {"id": "postpaid", "title": "Postpaid"}
                                ] if t['id'] == type_id),
                                "Unknown Type"
                            )
                            user_electricity_state[phone_number] = {
                                "step": "meter",
                                "provider": state["provider"],
                                "payment_type": type_title
                            }
                            response = ask_meter_number(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Electricity step handled", 200)
                    elif state["step"] == "meter":
                        if message.get('type') == 'text':
                            meter_number = message['text']['body']
                            user_electricity_state[phone_number] = {
                                "step": "amount",
                                "provider": state["provider"],
                                "payment_type": state["payment_type"],
                                "meter_number": meter_number
                            }
                            response = ask_electricity_amount(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Electricity step handled", 200)
                    elif state["step"] == "amount":
                        if message.get('type') == 'text':
                            amount = message['text']['body']
                            try:
                                float(amount)
                                user_electricity_state[phone_number] = {
                                    "step": "confirm",
                                    "provider": state["provider"],
                                    "payment_type": state["payment_type"],
                                    "meter_number": state["meter_number"],
                                    "amount": amount
                                }
                                response = confirm_electricity_payment(
                                    phone_number,
                                    state["provider"],
                                    state["payment_type"],
                                    state["meter_number"],
                                    amount
                                )
                                send_whatsapp_message(phone_number, response["text"]["body"])
                            except ValueError:
                                send_whatsapp_message(phone_number, "❌ Invalid amount. Please enter a valid number.")
                        return make_response("Electricity step handled", 200)
                    elif state["step"] == "confirm":
                        if message.get('type') == 'text' and message['text']['body'].strip().lower() == 'confirm':
                            response = electricity_payment_completed(
                                phone_number,
                                state["provider"],
                                state["meter_number"],
                                state["amount"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            del user_electricity_state[phone_number]
                        else:
                            send_whatsapp_message(phone_number, "❌ Payment cancelled. Type 'CONFIRM' to complete the payment.")
                        return make_response("Electricity step handled", 200)

                # Cable TV bill
                if phone_number in user_cable_state:
                    state = user_cable_state[phone_number]
                    if state["step"] == "provider":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            provider_id = message['interactive']['list_reply']['id']
                            provider_title = next(
                                (p['title'] for p in [
                                    {"id": "dstv", "title": "DSTV"},
                                    {"id": "gotv", "title": "GOTV"}
                                ] if p['id'] == provider_id),
                                "Unknown Provider"
                            )
                            user_cable_state[phone_number] = {
                                "step": "package",
                                "provider": provider_title
                            }
                            response = ask_cable_package(phone_number, provider_title.lower())
                            send_whatsapp_interactive(phone_number, response)
                        return make_response("Cable step handled", 200)
                    elif state["step"] == "package":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            package_id = message['interactive']['list_reply']['id']
                            package_title = next(
                                (p['title'] for p in [
                                    {"id": "dstv_box_office", "title": "Box Office - ₦5,000"},
                                    {"id": "dstv_compact", "title": "Compact - ₦10,000"},
                                    {"id": "dstv_premium", "title": "Premium - ₦20,000"},
                                    {"id": "gotv_lite", "title": "Lite - ₦2,000"},
                                    {"id": "gotv_max", "title": "Max - ₦5,000"},
                                    {"id": "gotv_supa", "title": "Supa - ₦8,000"}
                                ] if p['id'] == package_id),
                                "Unknown Package"
                            )
                            user_cable_state[phone_number] = {
                                "step": "smartcard",
                                "provider": state["provider"],
                                "package": package_title
                            }
                            response = ask_smartcard_number(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Cable step handled", 200)
                    elif state["step"] == "smartcard":
                        if message.get('type') == 'text':
                            smartcard_number = message['text']['body']
                            user_cable_state[phone_number] = {
                                "step": "confirm",
                                "provider": state["provider"],
                                "package": state["package"],
                                "smartcard_number": smartcard_number
                            }
                            response = confirm_cable_payment(
                                phone_number,
                                state["provider"],
                                state["package"],
                                smartcard_number
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Cable step handled", 200)
                    elif state["step"] == "confirm":
                        if message.get('type') == 'text' and message['text']['body'].strip().lower() == 'confirm':
                            response = cable_payment_completed(
                                phone_number,
                                state["provider"],
                                state["package"],
                                state["smartcard_number"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            del user_cable_state[phone_number]
                        else:
                            send_whatsapp_message(phone_number, "❌ Payment cancelled. Type 'CONFIRM' to complete the payment.")
                        return make_response("Cable step handled", 200)

                # Education bill
                if phone_number in user_education_state:
                    state = user_education_state[phone_number]
                    if state["step"] == "biller":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            biller_id = message['interactive']['list_reply']['id']
                            biller_title = next(
                                (b['title'] for b in [
                                    {"id": "waec", "title": "WAEC"}
                                ] if b['id'] == biller_id),
                                "Unknown Biller"
                            )
                            user_education_state[phone_number] = {
                                "step": "package",
                                "biller": biller_title
                            }
                            response = ask_waec_package(phone_number)
                            send_whatsapp_interactive(phone_number, response)
                        return make_response("Education step handled", 200)
                    elif state["step"] == "package":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            package_id = message['interactive']['list_reply']['id']
                            package_title = next(
                                (p['title'] for p in [
                                    {"id": "waec_1", "title": "1 PIN - ₦1,000"},
                                    {"id": "waec_2", "title": "2 PINs - ₦1,900"},
                                    {"id": "waec_5", "title": "5 PINs - ₦4,500"}
                                ] if p['id'] == package_id),
                                "Unknown Package"
                            )
                            user_education_state[phone_number] = {
                                "step": "phone",
                                "biller": state["biller"],
                                "package": package_title
                            }
                            response = ask_beneficiary_phone(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Education step handled", 200)
                    elif state["step"] == "phone":
                        if message.get('type') == 'text':
                            beneficiary_phone = message['text']['body']
                            if len(beneficiary_phone) >= 10 and beneficiary_phone.isdigit():
                                user_education_state[phone_number] = {
                                    "step": "confirm",
                                    "biller": state["biller"],
                                    "package": state["package"],
                                    "beneficiary_phone": beneficiary_phone
                                }
                                response = confirm_education_payment(
                                    phone_number,
                                    state["biller"],
                                    state["package"],
                                    beneficiary_phone
                                )
                                send_whatsapp_message(phone_number, response["text"]["body"])
                            else:
                                send_whatsapp_message(phone_number, "❌ Invalid phone number. Please enter a valid 10 or 11 digit number.")
                        return make_response("Education step handled", 200)
                    elif state["step"] == "confirm":
                        if message.get('type') == 'text' and message['text']['body'].strip().lower() == 'confirm':
                            response = education_payment_completed(
                                phone_number,
                                state["biller"],
                                state["package"],
                                state["beneficiary_phone"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            del user_education_state[phone_number]
                        else:
                            send_whatsapp_message(phone_number, "❌ Payment cancelled. Type 'CONFIRM' to complete the payment.")
                        return make_response("Education step handled", 200)

                # Betting bill
                if phone_number in user_betting_state:
                    state = user_betting_state[phone_number]
                    if state["step"] == "platform":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            platform_id = message['interactive']['list_reply']['id']
                            platform_title = next(
                                (p['title'] for p in [
                                    {"id": "sporty", "title": "SportyBet"},
                                    {"id": "paripesa", "title": "Paripesa"},
                                    {"id": "bet9ja", "title": "Bet9ja"}
                                ] if p['id'] == platform_id),
                                "Unknown Platform"
                            )
                            user_betting_state[phone_number] = {
                                "step": "customer_id",
                                "platform": platform_title
                            }
                            response = ask_customer_id(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Betting step handled", 200)
                    elif state["step"] == "customer_id":
                        if message.get('type') == 'text':
                            customer_id = message['text']['body']
                            user_betting_state[phone_number] = {
                                "step": "confirm",
                                "platform": state["platform"],
                                "customer_id": customer_id
                            }
                            response = confirm_betting_payment(
                                phone_number,
                                state["platform"],
                                customer_id
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                        return make_response("Betting step handled", 200)
                    elif state["step"] == "confirm":
                        if message.get('type') == 'text' and message['text']['body'].strip().lower() == 'confirm':
                            response = betting_payment_completed(
                                phone_number,
                                state["platform"],
                                state["customer_id"]
                            )
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            del user_betting_state[phone_number]
                        else:
                            send_whatsapp_message(phone_number, "❌ Payment cancelled. Type 'CONFIRM' to complete the payment.")
                        return make_response("Betting step handled", 200)

                # Bill type selection
                if phone_number in user_bill_state:
                    state = user_bill_state[phone_number]
                    if state["step"] == "bill_type":
                        if message.get('type') == 'interactive' and message['interactive']['type'] == 'list_reply':
                            bill_type = message['interactive']['list_reply']['id']
                            if bill_type == "electricity":
                                user_electricity_state[phone_number] = {"step": "provider"}
                                response = ask_electricity_provider(phone_number)
                                send_whatsapp_interactive(phone_number, response)
                            elif bill_type == "cable_tv":
                                user_cable_state[phone_number] = {"step": "provider"}
                                response = ask_cable_provider(phone_number)
                                send_whatsapp_interactive(phone_number, response)
                            elif bill_type == "education":
                                user_education_state[phone_number] = {"step": "biller"}
                                response = ask_education_biller(phone_number)
                                send_whatsapp_interactive(phone_number, response)
                            elif bill_type == "betting":
                                user_betting_state[phone_number] = {"step": "platform"}
                                response = ask_betting_platform(phone_number)
                                send_whatsapp_interactive(phone_number, response)
                            del user_bill_state[phone_number]
                        return make_response("Bill type selected", 200)

                # --- Menu selection handling ---
                if message.get("type") == "interactive":
                    interactive = message.get("interactive", {})
                    if interactive.get("type") == "list_reply":
                        selected_id = interactive["list_reply"]["id"]

                        # Start transfer process
                        if selected_id == "transfer_money":
                            user_transfer_state[phone_number] = {"step": "amount"}
                            response = ask_transfer_amount(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            return make_response("Transfer started", 200)

                        # Start airtime process
                        if selected_id == "buy_airtime":
                            user_airtime_state[phone_number] = {"step": "phone"}
                            response = ask_airtime_phone_number(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            return make_response("Airtime purchase started", 200)

                        # Start data purchase process
                        if selected_id == "buy_data":
                            user_data_state[phone_number] = {"step": "phone"}
                            response = ask_data_phone_number(phone_number)
                            send_whatsapp_message(phone_number, response["text"]["body"])
                            return make_response("Data purchase started", 200)

                        # Start bill payment process
                        if selected_id == "pay_bills":
                            user_bill_state[phone_number] = {"step": "bill_type"}
                            response = handle_pay_bills(phone_number, profile_name)
                            send_whatsapp_interactive(phone_number, response)
                            return make_response("Bill payment started", 200)

                        # Other menu items
                        menu_response = handle_menu_selection(selected_id, phone_number, profile_name)
                        if menu_response.get("type") == "text":
                            send_whatsapp_message(phone_number, menu_response["text"]["body"])
                        elif menu_response.get("type") == "interactive":
                            send_whatsapp_interactive(phone_number, menu_response)
                        return make_response("Menu handled", 200)

                # --- Form submission handling (your existing code) ---
                interactive = message.get("interactive", {})
                if interactive.get("type") == "nfm_reply":
                    try:
                        form_data = interactive["nfm_reply"]["response_json"]
                        if isinstance(form_data, str):
                            form_data = json.loads(form_data)
                        
                        # Capture navigation actions too
                        if "navigate" in form_data:
                            # Extract payload from navigation action
                            nav_data = form_data.get("navigate", {}).get("payload", {})
                            if nav_data:
                                print(f"🚦 Captured navigation data: {json.dumps(nav_data, indent=2)}")
                                save_user_data(phone_number, profile_name, nav_data)
                        
                        # Always save the form data
                        print(f"📝 Form data: {json.dumps(form_data, indent=2)}")
                        success = save_user_data(phone_number, profile_name, form_data)
                        
                        if success:
                            print(f"📊 Saved data for {phone_number}")
                            # Send welcome message with user data UPDATE TO ACTUAL BALANCE AND ACCOUNT NUMBER
                            msg_payload = welcome_message(profile_name, "3298868791", 0.00)
                            send_whatsapp_interactive(phone_number, msg_payload)
                        else:
                            print("❌ Failed to save user data")
                        
                        return make_response("Data saved", 200)
                        
                    except Exception as e:
                        print("❌ Error processing form data:", e)
                        return make_response("Error processing form", 500)
                
                # Send flow template if not form submission
                send_whatsapp_template(to=phone_number, user_name=profile_name)
            return make_response("Message processed", 200)
        except Exception as e:
            print("❌ Error processing message:", e)
            return make_response("Error", 500)

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
                    "flow_name": "signup_flow",
                    "flow_cta": "Get Started",
                }
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    print("\n📤 WhatsApp API Response:", response.json())
    return response.json()

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
        **interactive_payload  # Unpack the interactive structure
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"📤 WhatsApp interactive message status: {response.status_code} | {response.text}")

@app.route("/test")
def test():
    return "Test endpoint is working!", 200

user_transfer_state = {}
user_airtime_state = {}
user_data_state = {}
user_bill_state = {}
user_electricity_state = {}
user_cable_state = {}
user_education_state = {}
user_betting_state = {}

def handle_buy_data(phone_number, profile_name):
    return ask_data_phone_number(phone_number)