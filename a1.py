import random
import os
from datetime import datetime
import platform

accounts = {}

# -----------------------------
# Utility Functions
# -----------------------------

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def generate_account_number():
    while True:
        acc_no = str(random.randint(10000, 99999))
        if acc_no not in accounts:
            return acc_no

def log_transaction(acc_no, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[acc_no]["transactions"].append(f"{timestamp} - {message}")

def load_from_file(filename="accounts.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                try:
                    acc_no, name, pin, balance, txn_str = line.strip().split("|")
                    accounts[acc_no] = {
                        "name": name,
                        "pin": pin,
                        "balance": float(balance),
                        "transactions": txn_str.split("#") if txn_str else []
                    }
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")

def save_to_file(filename="accounts.txt"):
    with open(filename, "w") as f:
        for acc_no, info in accounts.items():
            f.write(f"{acc_no}|{info['name']}|{info['pin']}|{info['balance']}|{'#'.join(info['transactions'])}\n")

# -----------------------------
# Admin Functions
# -----------------------------

def admin_menu():
    while True:
        clear_screen()
        print("\n--- Admin Menu ---")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. View All Transactions")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            view_all_accounts()
        elif choice == "3":
            view_all_transactions()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def create_account():
    name = input("Enter account holder name: ").strip()
    if any(char.isdigit() for char in name):
        print("Name cannot contain numbers.")
        return
    pin = input("Set a 4-digit PIN: ").strip()
    if not pin.isdigit() or len(pin) != 4:
        print("PIN must be exactly 4 digits.")
        return
    try:
        initial_balance = float(input("Enter initial balance: "))
        if initial_balance < 0:
            print("Initial balance must be non-negative.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    acc_no = generate_account_number()
    accounts[acc_no] = {
        "name": name,
        "pin": pin,
        "balance": initial_balance,
        "transactions": []
    }
    log_transaction(acc_no, f"Account created with balance {initial_balance}")
    save_to_file()
    print(f"Account created successfully! Account Number: {acc_no}")

def view_all_accounts():
    if not accounts:
        print("No accounts available.")
        return
    print("\n--- All Accounts ---")
    for acc_no, info in accounts.items():
        print(f"Account Number: {acc_no}, Name: {info['name']}, Balance: {info['balance']}")

def view_all_transactions():
    if not accounts:
        print("No accounts available.")
        return
    print("\n--- All Transactions ---")
    for acc_no, info in accounts.items():
        print(f"\nAccount Number: {acc_no}")
        for txn in info['transactions']:
            print("-", txn)

# -----------------------------
# Customer Functions
# -----------------------------

def customer_menu(acc_no):
    while True:
        clear_screen()
        print(f"\n--- Welcome {accounts[acc_no]['name']} ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. View Transactions")
        print("5. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            deposit_money(acc_no)
        elif choice == "2":
            withdraw_money(acc_no)
        elif choice == "3":
            check_balance(acc_no)
        elif choice == "4":
            transaction_history(acc_no)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def deposit_money(acc_no):
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        accounts[acc_no]["balance"] += amount
        log_transaction(acc_no, f"Deposited {amount}")
        save_to_file()
        print("Deposit successful.")
    except ValueError:
        print("Invalid amount.")

def withdraw_money(acc_no):
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        if accounts[acc_no]["balance"] >= amount:
            accounts[acc_no]["balance"] -= amount
            log_transaction(acc_no, f"Withdrew {amount}")
            save_to_file()
            print("Withdrawal successful.")
        else:
            print("Insufficient balance.")
    except ValueError:
        print("Invalid amount.")

def check_balance(acc_no):
    print(f"Current Balance: {accounts[acc_no]['balance']}")

def transaction_history(acc_no):
    print("Transaction History:")
    for txn in accounts[acc_no]["transactions"]:
        print("-", txn)

# -----------------------------
# Main Program
# -----------------------------

def main():
    load_from_file()
    while True:
        print("\n=== Welcome to Mini Banking App ===")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Exit")
        role = input("Select role: ")

        if role == "1":
            pwd = input("Enter admin password: ")
            if pwd == "admin123":
                admin_menu()
            else:
                print("Incorrect password.")
        elif role == "2":
            acc_no = input("Enter your account number: ").strip()
            if acc_no in accounts:
                pin = input("Enter your 4-digit PIN: ").strip()
                if accounts[acc_no]["pin"] == pin:
                    customer_menu(acc_no)
                else:
                    print("Incorrect PIN.")
            else:
                print("Account not found.")
        elif role == "3":
            save_to_file()
            print("Thank you for using the Mini Banking App!")
            break
        else:
            print("Invalid option. Try again.")
main()