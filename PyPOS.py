from datetime import datetime

item_names=[]
item_prices=[]
item_codes=[]
scanned_items = []
scanned_prices = []
total = 0
money = 0
change = 0
currency=""
configcommands=["Currency", "CashierModeOnLaunch", "DefaultDataFile", "AlwaysSaveTransactionLogs"]
AlwaysSaveTransactionLogs = False
configdatatype=["str", "bool", "str"]

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
    money = 0
    change = 0
    user_input = ""
    while user_input != "continue":
        user_input = input("Enter item codes or scan the bar code (or type 'continue' to finish, *(number) to enter quantity, or exit to exit cashier mode): ")
        if user_input == "exit":
            print("Exiting cashier mode.")
            return       
        elif user_input in item_codes:
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
    money = input("Enter the amount of money given by the customer (or cancel to cancel the transaction): ")
    if money == "cancel":
        print("Transaction canceled.")
        return
    else:
        change = float(money) - total
        print(f"Change: {change:.2f}{currency}")
        if AlwaysSaveTransactionLogs:
            save_transaction_log()
        else:
            user_input = input("Save transaction logs? (y/n): ")
            if user_input.lower() == "y":
                save_transaction_log()
        
    cashier()

def save_transaction_log():
    timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    filename = f"transaction_log_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write("Transaction Log\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Scanned Items: {scanned_items}\n")
        f.write(f"Total Price: {total:.2f}{currency}\n")
        f.write(f"Money Given: {money}{currency}\n")
        f.write(f"Change: {change:.2f}{currency}\n")
        print(f"Transaction log saved to {filename}.")

def list():
    print("Listing all items:")
    for i in range(len(item_codes)):
        print(f"Item Code: {item_codes[i]}, Item Name: {item_names[i]}, Price: {item_prices[i]:.2f}{currency}")

def currency(curr):
    global currency
    currency = curr
    print(f"Currency set to {currency}.")
    
print("░       ░░░  ░░░░  ░░       ░░░░      ░░░░      ░░")
print("▒  ▒▒▒▒  ▒▒▒  ▒▒  ▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒")
print("▓       ▓▓▓▓▓    ▓▓▓▓       ▓▓▓  ▓▓▓▓  ▓▓▓      ▓▓")
print("█  ███████████  █████  ████████  ████  ████████  █")
print("█  ███████████  █████  █████████      ████      ██")
print("")
print("Welcome to PyPOS!")

try:
    with open("config.txt", "r") as f:
        config = f.read()
        config = config.replace("\n", " ")
        config = config.replace("=", " ")
        data = config.split()
        for i in range(0, len(data), 2):
            if data[i] in configcommands:
                if data[i] == str(configcommands[0]):
                    currency = data[i + 1]
                elif data[i] == str(configcommands[1]):
                    if data[i + 1].lower() == "true":
                        cashier()
                elif data[i] == str(configcommands[2]):
                    load(data[i + 1])
                elif data[i] == str(configcommands[3]):
                    if data[i + 1].lower() == "true":
                        AlwaysSaveTransactionLogs = True
            else:
                continue
except FileNotFoundError:
    print("Config file not found. Please create a config.txt file with the necessary settings.")

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