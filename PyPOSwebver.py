from datetime import datetime
import streamlit as st
import pandas as pd
item_names=[]
item_prices=[]
item_codes=[]
currency=""
df=pd.DataFrame()

def load(filename):
    global df
    try:
        with open(filename, "r") as f:
            temp = f.read()
            temp = temp.replace("\n", " ")
            temp = temp.replace(":", " ")
            data = temp.split()
            for i in range(0, len(data), 3):
                item_codes.append(data[i])
                item_names.append(data[i + 1])
                item_prices.append(float(data[i + 2]))
            dic = {"Item Codes": item_codes, "Item Names": item_names, "Item Prices": item_prices}
            df = pd.DataFrame(dic)
            f.close()
            st.write("Item data loaded successfully.")
            st.write(df)
    except FileNotFoundError:
            st.write("File not found.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

def cashier():
    st.write("Entering cashier mode...")
    if "scanned_items" not in st.session_state:
        st.session_state.scanned_items = []
        st.session_state.scanned_prices = []
        st.session_state.cashier_finished = False

    with st.form("scan_item_form", clear_on_submit=True):
        item_code = st.text_input("Enter item code or scan the bar code:")
        quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
        add_item = st.form_submit_button("Add Item")

    if add_item:
        if item_code in item_codes:
            index = item_codes.index(item_code)
            item_price = item_prices[index] * quantity
            st.session_state.scanned_items.append(
                f"{item_names[index]} x{quantity}"
            )
            st.session_state.scanned_prices.append(item_price)
        else:
            st.error("Item code not found. Please try again.")

    total = sum(st.session_state.scanned_prices)

    for item, price in zip(
        st.session_state.scanned_items,
        st.session_state.scanned_prices
    ):
        st.write(f"Scanned Item: {item}, Price: {price:.2f}{currency}")

    st.write(f"Total Price: {total:.2f}{currency}")

    if st.button("Continue", key="continue_cashier"):
        st.session_state.cashier_finished = True

    if not st.session_state.cashier_finished:
        return

    money=st.text_input("Enter the amount of money given by the customer (or cancel to cancel the transaction): ")
    if money == "cancel":
        st.write("Transaction canceled.")
        return
    else:
        change = float(money) - total
        st.write(f"Change: {change:.2f}{currency}")
        save_log = st.button("Yes, save transaction log", key="save_log_yes")
        skip_log = st.button("No, do not save transaction log", key="save_log_no")
        if save_log:
            with open("transaction_logs.txt", "a") as log_file:
                log_file.write(f"{datetime.now()}: Scanned Items: {st.session_state.scanned_items}, Total Price: {total:.2f}{currency}, Money Given: {money}, Change: {change:.2f}{currency}\n")
            st.write("Transaction logs saved.")
        elif skip_log:
            st.write("Transaction log not saved.")

    continue_cashier = st.button("Yes, continue cashier mode", key="continue_cashier_yes")
    exit_cashier = st.button("No, exit cashier mode", key="continue_cashier_no")
    if continue_cashier:
        cashier()
    elif exit_cashier:
        st.write("Exiting cashier mode.")

def list():
    st.write("Listing all items:")
    st.dataframe(df)

def set_currency(curr):
    global currency
    currency = curr
    st.write(f"Currency set to {currency}.")



st.title("PyPOS")
st.write("Welcome to PyPOS!")

if "page" not in st.session_state:
    st.session_state.page = "menu"

if st.button("Load Item Data"):
    st.session_state.page = "load"
if st.button("Cashier Mode"):
    st.session_state.page = "cashier"
if st.button("List Items"):
    st.session_state.page = "list"
if st.button("Set Currency"):
    st.session_state.page = "currency"
if st.button("Exit"):
    st.session_state.page = "exit"

if st.session_state.page == "load":
    fnm = st.text_input("Enter the filename to load item data from:")
    if st.button("Load", key="load_items"):
        load(fnm)
elif st.session_state.page == "cashier":
    cashier()
elif st.session_state.page == "list":
    list()
elif st.session_state.page == "currency":
    curr = st.text_input("Enter the currency:")
    if st.button("Set", key="set_currency"):
        set_currency(curr)
elif st.session_state.page == "exit":
    st.write("Exiting PyPOS. Goodbye!")