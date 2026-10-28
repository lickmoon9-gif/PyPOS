from datetime import datetime
from escpos.printer import Usb
from escpos.printer import Serial 
from fpdf import FPDF

item_names=[]
item_prices=[]
item_codes=[]
scanned_items = []
scanned_prices = []
total = 0
money = 0
change = 0
PrinterBaudRate = 0
currency=""
PrinterType = ""
PrinterVendorID = ""
PrinterProductID = ""
PrinterSerialPort = ""
PrinterProfile = ""
TransactionLogFileFormat="txt"
dsrdtr = True
AlwaysSaveTransactionLogs = False
AlwaysPrintReceipts = False

configcommands=["Currency", "CashierModeOnLaunch", "DefaultDataFile", "AlwaysSaveTransactionLogs", "PrinterType", "PrinterVendorID", "PrinterProductID", "PrinterSerialPort", "PrinterBaudRate","dsrdtr","PrinterProfile", "AlwaysPrintReciepts", "TransactionLogFileFormat"]


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
        user_input = input("Enter item codes or scan the bar code (or type 'continue' to finish, *(number) to enter quantity, remove ProductCode to remove product from purchase, exit to exit cashier mode): ")
        if user_input == "exit":
            print("Exiting cashier mode.")
            return       
        elif user_input in item_codes:
            index = item_codes.index(user_input)
            print(f"Item: {item_names[index]}, Price: {item_prices[index]:.2f}{currency}")
            total += item_prices[index]
            scanned_items.append(item_names[index])
            scanned_prices.append(item_prices[index])
        elif user_input.startswith("remove"):  # Remove "remove(" and ")"
            if user_input in scanned_items:
                temp = scanned_items.index(user_input)
                del scanned_items[temp]
                del scanned_prices[temp]
                print(f"Removed {user_input[i + 1]} from the purchase.")
            else:
                print(f"{user_input[i + 1]} not found in the purchase.")                
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
            if TransactionLogFileFormat == "txt":
                save_transaction_log_txt()
            elif TransactionLogFileFormat == "pdf":
                save_transaction_log_pdf
            elif TransactionLogFileFormat == "both":
                save_transaction_log_txt()
                save_transaction_log_pdf()
        else:
            user_input = input("Save transaction logs? (y/n): ")
            if user_input.lower() == "y":
                if TransactionLogFileFormat == "txt":
                    save_transaction_log_txt()
                elif TransactionLogFileFormat == "pdf":
                    save_transaction_log_pdf
                elif TransactionLogFileFormat == "both":
                    save_transaction_log_txt()
                    save_transaction_log_pdf()
    if AlwaysPrintReceipts:
        print_receipt()
    else:
        user_input = input("Print receipt? (y/n): ")
        if user_input.lower() == "y":
            print_receipt()
        
    cashier()

def save_transaction_log_txt():
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

def save_transaction_log_pdf():
    timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Transaction Log", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Timestamp: {timestamp}", ln=True, align="L")
    for i in range(len(scanned_items)):
        pdf.cell(200, 10, txt=f"Scanned Items: {scanned_items[i]}, Price: {scanned_prices[i]:.2f}{currency}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Total Price: {total:.2f}{currency}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Money Given: {money}{currency}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Change: {change:.2f}{currency}", ln=True, align="L")
    pdf.output(f"transaction_log_{timestamp}.pdf")
    print(f"Transaction log saved to transaction_log_{timestamp}.pdf.")

def list():
    print("Listing all items:")
    for i in range(len(item_codes)):
        print(f"Item Code: {item_codes[i]}, Item Name: {item_names[i]}, Price: {item_prices[i]:.2f}{currency}")

def currency(curr):
    global currency
    currency = curr
    print(f"Currency set to {currency}.")

def printer_setup():
    global PrinterType, PrinterVendorID, PrinterProductID, PrinterSerialPort, PrinterBaudRate, dsrdtr, PrinterProfile
    PrinterType = input("Enter printer type (USB/Serial): ")
    if PrinterType.lower() == "usb":
        PrinterVendorID = input("Enter USB printer vendor ID: ")
        PrinterProductID = input("Enter USB printer product ID: ")
        PrinterProfile = input("Enter USB printer profile (default: 'default'): ")
    elif PrinterType.lower() == "serial":
        PrinterSerialPort = input("Enter serial printer port (e.g., COM3 or /dev/ttyS0): ")
        PrinterBaudRate = int(input("Enter serial printer baud rate (e.g., 9600): "))
        dsrdtr_input = input("Enable DSR/DTR flow control? (true/false): ")
        dsrdtr = dsrdtr_input.lower() == "true"
        PrinterProfile = input("Enter serial printer profile: ")
    else:
        print("Invalid printer type. Please enter either 'USB' or 'Serial'.")

def print_receipt():
    if PrinterType.lower() == "usb":
        try:
            p = Usb(int(PrinterVendorID), int(PrinterProductID), 0, profile=PrinterProfile)
            for i in range(len(scanned_items)):
                p.text(f"Item: {scanned_items[i]}, Price: {scanned_prices[i]:.2f}{currency}\n")
            p.text(f"Total Price: {total:.2f}{currency}\n")
            p.text(f"Money Given: {money}{currency}\n")
            p.text(f"Change: {change:.2f}{currency}\n")
            p.cut()
        except Exception as e:
            print(f"Error occurred while initializing USB printer: {e}")
    elif PrinterType.lower() == "serial":
        try:
            p = Serial(
                devfile=PrinterSerialPort,
                baudrate=PrinterBaudRate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1.00,
                dsrdtr=dsrdtr,
                profile=PrinterProfile
            ) 
            for i in range(len(scanned_items)):
                p.text(f"Item: {scanned_items[i]}, Price: {scanned_prices[i]:.2f}{currency}\n")
            p.text(f"Total Price: {total:.2f}{currency}\n")
            p.text(f"Money Given: {money}{currency}\n")
            p.text(f"Change: {change:.2f}{currency}\n")
            p.cut()
        except Exception as e:
            print(f"Error occurred while initializing Serial printer: {e}")

def test_printer():
    if PrinterType.lower() == "usb":
        try:
            p = Usb(int(PrinterVendorID), int(PrinterProductID), 0, profile=PrinterProfile)
            p.text("Test Print\n")
            while True:
                p.print(f"Vendor ID: {PrinterVendorID}\n")
                p.print(f"Product ID: {PrinterProductID}\n")
                p.print(f"Profile: {PrinterProfile}\n")   
                p.cut()
                break 
            print("Test print sent to USB printer.")
        except Exception as e:
            print(f"Error occurred while testing USB printer: {e}")
    elif PrinterType.lower() == "serial":
        try:
            p = Serial(
                devfile=PrinterSerialPort,
                baudrate=PrinterBaudRate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1.00,
                dsrdtr=dsrdtr,
                profile=PrinterProfile
            ) 
            while True:
                p.print("Test Print\n")
                p.print(f"Serial Port: {PrinterSerialPort}\n")
                p.print(f"Baud Rate: {PrinterBaudRate}\n")
                p.print(f"DSR/DTR: {dsrdtr}\n")
                p.print(f"Profile: {PrinterProfile}\n")   
                break
            p.cut()
            print("Test print sent to Serial printer.")
        except Exception as e:
            print(f"Error occurred while testing Serial printer: {e}")

print("░       ░░░  ░░░░  ░░       ░░░░      ░░░░      ░░")
print("▒  ▒▒▒▒  ▒▒▒  ▒▒  ▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒")
print("▓       ▓▓▓▓▓    ▓▓▓▓       ▓▓▓  ▓▓▓▓  ▓▓▓      ▓▓")
print("█  ███████████  █████  ████████  ████  ████████  █")
print("█  ███████████  █████  █████████      ████      ██")
print("")
print("Welcome to PyPOS!")

try:
    with open("config.txt", "r") as f:
        data = []
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            data.extend(line.replace("=", " ").split())
        for i in range(0, len(data), 2):
            if data[i] in configcommands:
                if data[i] == str(configcommands[0]):
                    try:
                        currency = data[i + 1]
                    except IndexError:
                        print("Invalid config value for currency.")
                elif data[i] == str(configcommands[1]):
                    try:
                        if data[i + 1].lower() == "true":
                            cashier()
                    except IndexError:
                        print("Invalid config value for cashier.")
                elif data[i] == str(configcommands[2]):
                    try:
                        load(data[i + 1])
                    except IndexError:
                        print("Invalid config value for load.")
                    except FileNotFoundError:
                        print(f"Data file '{data[i + 1]}' not found.")
                elif data[i] == str(configcommands[3]):
                    try:
                        AlwaysSaveTransactionLogs = data[i + 1].lower() == "true"
                    except IndexError:
                        print("Invalid config value for AlwaysSaveTransactionLogs.")
                elif data[i] == str(configcommands[4]):
                    try:
                        PrinterType = data[i + 1]
                    except IndexError:
                        print("Invalid config value for PrinterType.")
                elif data[i] == str(configcommands[5]):
                    try:
                        PrinterVendorID = data[i + 1]
                    except IndexError:
                        print("Invalid config value for PrinterVendorID.")
                elif data[i] == str(configcommands[6]):
                    try:
                        PrinterProductID = data[i + 1]
                    except IndexError:
                        print("Invalid config value for PrinterProductID.")
                elif data[i] == str(configcommands[7]):
                    try:
                        PrinterSerialPort = data[i + 1]
                    except IndexError:
                        print("Invalid config value for PrinterSerialPort.")
                elif data[i] == str(configcommands[8]):
                    try:
                        PrinterBaudRate = int(data[i + 1])
                    except IndexError:
                        print("Invalid config value for PrinterBaudRate.")
                    except ValueError:
                        print("PrinterBaudRate must be an integer.")
                elif data[i] == str(configcommands[9]):
                    try:
                        dsrdtr = data[i + 1].lower() == "true"
                    except IndexError:
                        print("Invalid config value for dsrdtr.")
                elif data[i] == str(configcommands[10]):
                    try:
                        PrinterProfile = data[i + 1]
                    except IndexError:
                        print("Invalid config value for PrinterProfile.")
                elif data[i] == str(configcommands[11]):
                    try:
                        if data[i + 1].lower() == "pdf":
                            TransactionLogFileFormat = "pdf"
                        elif data[i + 1].lower() == "txt":
                            TransactionLogFileFormat = "txt"
                        elif data[i + 1].lower() == "both":
                            TransactionLogFileFormat = "both"
                    except IndexError:
                        print("Invalid config value for TransactionLogFileFormat")
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
    elif inpt == "printer_setup":
        printer_setup()
    elif inpt == "always_print_receipts":
        AlwaysPrintReceipts = not AlwaysPrintReceipts
        print(f"AlwaysPrintReceipts set to {AlwaysPrintReceipts}.")
    elif inpt.startswith("tlff"):
        inpt = inpt.split(" ")
        if inpt[1] == "txt":
            TransactionLogFileFormat = "txt"
            print(f"Transaction log file format set to {TransactionLogFileFormat}")
        elif inpt[1] == "pdf":
            TransactionLogFileFormat = "pdf"
            print(f"Transaction log file format set to {TransactionLogFileFormat}")
        elif inpt[1] == "both":
            TransactionLogFileFormat = "both"
        else:
            print("Invalid transaction log file format. Please use 'txt', 'pdf', or 'both'.")