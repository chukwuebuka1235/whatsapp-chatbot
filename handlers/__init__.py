from .transfer import handle_transfer_money
from .airtime import handle_buy_airtime
from .data import handle_buy_data
from .bills import handle_pay_bills
from .balance import handle_check_balance
from .history import handle_transaction_history

def handle_menu_selection(selected_id, phone_number, profile_name):
    if selected_id == "check_balance":
        return handle_check_balance(phone_number, profile_name)
    elif selected_id == "transfer_money":
        return handle_transfer_money(phone_number, profile_name)
    elif selected_id == "buy_airtime":
        return handle_buy_airtime(phone_number, profile_name)
    elif selected_id == "buy_data":
        return handle_buy_data(phone_number, profile_name)
    elif selected_id == "pay_bills":
        return handle_pay_bills(phone_number, profile_name)
    elif selected_id == "transaction_history":
        return handle_transaction_history(phone_number, profile_name)
    else:
        return {"error": "Invalid selection"}