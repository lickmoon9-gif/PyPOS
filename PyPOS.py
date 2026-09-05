from datetime import datetime

item_names=[]
item_prices=[]
item_codes=[]
currency=""

def load(filename):
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
            f.close()
            print("Item data loaded successfully.")
    except FileNotFoundError:
            print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def cashier():
    print("Entering cashier mode...")
    total = 0
    scanned_items = []
    scanned_prices = []
    user_input = ""
    while user_input != "continue":
        user_input = input("Enter item codes or scan the bar code (or type 'continue' to finish, or *(number) to enter quantity): ")
        if user_input in item_codes:
            index = item_codes.index(user_input)
            print(f"Item: {item_names[index]}, Price: {item_prices[index]:.2f}{currency}")
            total += item_prices[index]
            scanned_items.append(item_names[index])
            scanned_prices.append(item_prices[index])
        elif user_input.startswith("*"):
            quantity = int(user_input[1:])
            user_input = input("Enter item code to apply quantity: ")
            if user_input in item_codes:
                index = item_codes.index(user_input)
                print(f"Item: {item_names[index]}, Price: {item_prices[index]:.2f}{currency}, Quantity: {quantity}")
                total += item_prices[index] * quantity
                scanned_items.append(f"{item_names[index]} x{quantity}")
                scanned_prices.append(item_prices[index] * quantity)
            elif user_input != "continue":
                print("Item code not found. Please try again.")
        elif user_input != "continue":
            print("Item code not found. Please try again.")

    for i in range(len(scanned_items)):
        print(f"Scanned Item: {scanned_items[i]}, Price: {scanned_prices[i]:.2f}{currency}")

    print(f"Total Price: {total:.2f}{currency}")
    money=input("Enter the amount of money given by the customer (or cancel to cancel the transaction): ")
    if money == "cancel":
        print("Transaction canceled.")
        return
    else:
        change = float(money) - total
        print(f"Change: {change:.2f}{currency}")
        user_input = input("Save transaction logs? (y/n): ")
        if user_input.lower() == "y":
            try:
                with open("transaction_logs.txt", "a") as log_file:
                    log_file.write(f"{datetime.now()}: Scanned Items: {scanned_items}, Total Price: {total:.2f}{currency}, Money Given: {money}, Change: {change:.2f}{currency}\n")
                    log_file.close()
                    print("Transaction logs saved.")
            except FileNotFoundError:
                user_input = input("Transaction log file not found. Create a new one? (y/n): ")
                if user_input.lower() == "y":
                    with open("transaction_logs.txt", "w") as log_file:
                        log_file.write(f"{datetime.now()}: Scanned Items: {scanned_items}, Total Price: {total:.2f}{currency}, Money Given: {money}{currency}, Change: {change:.2f}{currency}\n")
                        print("Transaction logs saved.")
    user_input = input("Continue in cashier mode? (y/n): ")
    if user_input.lower() == "y":
        cashier()
    else:
        print("Exiting cashier mode.")

def list():
    print("Listing all items:")
    for i in range(len(item_codes)):
        print(f"Item Code: {item_codes[i]}, Item Name: {item_names[i]}, Price: {item_prices[i]:.2f}{currency}")

def currency(curr):
    currency = curr
    print(f"Currency set to {currency}.")



print("░       ░░░  ░░░░  ░░       ░░░░      ░░░░      ░░")
print("▒  ▒▒▒▒  ▒▒▒  ▒▒  ▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒")
print("▓       ▓▓▓▓▓    ▓▓▓▓       ▓▓▓  ▓▓▓▓  ▓▓▓      ▓▓")
print("█  ███████████  █████  ████████  ████  ████████  █")
print("█  ███████████  █████  █████████      ████      ██")
print("")
print("Welcome to PyPOS!")


while True:
    inpt = input(">>> ")
    if "load" in inpt:
        fnm = inpt.split(" ")[1]
        load(fnm)
    elif inpt == "exit":
        print("Exiting PyPOS. Goodbye!")
        break
    elif inpt == "cashier":
        cashier()
    elif inpt == "list":
        list()
    elif "currency" in inpt:
        curr = inpt.split(" ")[1]
        currency(curr)