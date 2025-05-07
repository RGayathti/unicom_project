import getpass
import datetime
import os


ACCOUNTS_FILE = 'AccountDetails.txt'
TRANSACTION_FILE = 'transactions.txt'
CREDENTIALS_FILE = 'credentials.txt'
ACCOUNT_NUM_FILE = 'account_numbers.txt'


accounts = {}


def load_data():
    """Load account and transaction data from files."""
    if os.path.exists(ACCOUNTS_FILE):
        f = open(ACCOUNTS_FILE, 'r')
        for line in f:
            parts = line.strip().split('|')
            acc_no = parts[0]
            name = parts[1]
            balance = float(parts[2])
            accounts[acc_no] = {'name': name, 'balance': balance, 'transactions': []}
        f.close()

    if os.path.exists(TRANSACTION_FILE):
        f = open(TRANSACTION_FILE, 'r')
        for line in f:
            acc_no, txn = line.strip().split('|')
            if acc_no in accounts:
                accounts[acc_no]['transactions'].append(txn)
        f.close()

def generate_account_number():
    """Generate a new unique account number."""
    if not os.path.exists(ACCOUNT_NUM_FILE):
        f = open(ACCOUNT_NUM_FILE, 'w')
        f.write('1001')
        f.close()

    f = open(ACCOUNT_NUM_FILE, 'r+')
    current = int(f.read().strip())
    new = current + 1
    f.seek(0)
    f.write(str(new))
    f.close()
    return str(current)

def write_account_details(acc_no, name, balance):
    """Save new account details to the file."""
    f = open(ACCOUNTS_FILE, 'a')
    f.write(acc_no + '|' + name + '|' + str(balance) + '\n')
    f.close()

def write_transaction(acc_no, txn):
    """Log a transaction to the transaction file."""
    f = open(TRANSACTION_FILE, 'a')
    f.write(acc_no + '|' + txn + '\n')
    f.close()


def createAccount():
    """Admin creates a new user account."""
    name = input("Enter Your Full Name : ").strip().upper()
    if name == '':
        print("Name cannot be empty.......")
        return

    try:
        balance = float(input("Enter Initial Balance: "))
        if balance < 0:
            print("Balance must be 0 or more.....")
            return
    except:
        print("Invalid input......")
        return

    acc_no = generate_account_number()
    username = "user" + acc_no
    password = "pass" + acc_no

    f = open(CREDENTIALS_FILE, 'a')
    f.write(username + ':' + password + ':user\n')
    f.close()

    accounts[acc_no] = {
        'name': name,
        'balance': balance,
        'transactions': [f"Account opened with Rs.{balance}"]
    }

    write_account_details(acc_no, name, balance)
    write_transaction(acc_no, f"Account opened with Rs.{balance}")
    print("Account Created Successfully......")
    print("Account Number:", acc_no)
    print("Username:", username)
    print("Password:", password)

def depositMoney():
    """Deposit money into an account."""
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Amount must be greater than 0.......")
            return
    except:
        print("Invalid input.......")
        return

    accounts[acc_no]['balance'] += amount
    save = f"Deposited Rs.{amount} on {datetime.datetime.now()}"
    accounts[acc_no]['transactions'].append(save)
    write_transaction(acc_no, save)
    print("Deposit Successful.......")

def withdrawMoney():
    """Withdraw money from an account."""
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Invalid amount......")
            return
    except:
        print("Wrong input.....")
        return

    if amount > accounts[acc_no]['balance']:
        print("Not enough balance.......")
        return

    accounts[acc_no]['balance'] -= amount
    save = f"Withdrew Rs.{amount} on {datetime.datetime.now()}"
    accounts[acc_no]['transactions'].append(save)
    write_transaction(acc_no, save)
    print("Withdraw Successful!.....")

def checkBalance():
    """Check the balance of an account."""
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.......")
        return
    print("Your Balance is Rs.", accounts[acc_no]['balance'])

def transactionHistory():
    """View the transaction history of an account."""
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.......")
        return
    print("Transaction History:")
    for t in accounts[acc_no]['transactions']:
        print("-", t)

def transferMoney():
    """Transfer money between accounts."""
    from_acc = input("Enter your Account Number: ").strip()
    if from_acc not in accounts:
        print("Source account not found.")
        return
    to_acc = input("Enter recipient Account Number: ").strip()
    if to_acc not in accounts:
        print("Recipient account not found.")
        return
    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except:
        print("Invalid input.")
        return

    if amount > accounts[from_acc]['balance']:
        print("Not enough balance.")
        return

    accounts[from_acc]['balance'] -= amount
    accounts[to_acc]['balance'] += amount
    from_txn = f"Transferred Rs.{amount} to {to_acc} on {datetime.datetime.now()}"
    to_txn = f"Received Rs.{amount} from {from_acc} on {datetime.datetime.now()}"
    accounts[from_acc]['transactions'].append(from_txn)
    accounts[to_acc]['transactions'].append(to_txn)
    write_transaction(from_acc, from_txn)
    write_transaction(to_acc, to_txn)
    print("Transfer Successful.")

def calculateInterest():
    """Calculate and add interest to an account."""
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return
    try:
        rate = float(input("Enter annual interest rate (in %): "))
        if rate < 0:
            print("Interest rate must be non-negative.")
            return
    except:
        print("Invalid input.")
        return

    balance = accounts[acc_no]['balance']
    interest = balance * (rate / 100)
    accounts[acc_no]['balance'] += interest
    txn = f"Interest of Rs.{interest} added on {datetime.datetime.now()}"
    accounts[acc_no]['transactions'].append(txn)
    write_transaction(acc_no, txn)
    print(f"Interest added. New Balance: Rs.{accounts[acc_no]['balance']}")




def read_credentials():
    """Read login credentials from the file."""
    creds = {}
    if os.path.exists(CREDENTIALS_FILE):
        f = open(CREDENTIALS_FILE, 'r')
        for line in f:
            line = line.strip()
            if line == '':
                continue
            username, password, role = line.split(':')
            creds[username] = {'password': password, 'role': role}
        f.close()
    return creds

def login(creds):
    """Handle user login and redirect to the appropriate menu."""
    attempt = 0
    while attempt < 3:
        username = input("Enter username: ")
        password = getpass.getpass("Enter your password: ")

        if username in creds and creds[username]['password'] == password:
            role = creds[username]['role']
            print("Login successful! You are a", role)
            if role == 'admin':
                adminMenu()
            elif role == 'user':
                userMenu()
        else:
            print("Login failed. Wrong credentials.........")
            attempt += 1
    if attempt == 3:
        print("Your attempts are finished.....")

def adminLogin(creds):
    """Handle admin login with validation."""
    attempt = 0
    while attempt < 3:
        username = input("Enter admin username: ").strip()
        password = getpass.getpass("Enter admin password: ").strip()

        if username in creds and creds[username]['password'] == password and creds[username]['role'] == 'admin':
            print("Admin login successful!")
            return True
        else:
            print("Invalid admin credentials. Please try again.")
            attempt += 1

    print("Too many failed attempts. Exiting...")
    return False



def adminMenu():
    """Display the admin menu."""
    while True:
        print("\nAdmin Menu")
        print("1. Create New Account")
        print("2. Logout")
        ch = input("Enter your choice: ")
        if ch == '1':
            createAccount()
        elif ch == '2':
            break
        else:
            print("Invalid option........")



def userMenu():
    """Display the user menu."""
    while True:
        print("\nUser Menu")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. View Transactions")
        print("5. Transfer Money")
        print("6. Calculate Interest")
        print("7. Logout")
        ch = input("Enter your choice: ")
        if ch == '1':
            depositMoney()
        elif ch == '2':
            withdrawMoney()
        elif ch == '3':
            checkBalance()
        elif ch == '4':
            transactionHistory()
        elif ch == '5':
            transferMoney()
        elif ch == '6':
            calculateInterest()
        elif ch == '7':
            break
        else:
            print("Invalid option.......")

def mainMenu():
    """Display the main menu for the program."""
    while True:
        print("\nMain Menu")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Transfer Money")
        print("7. Calculate Interest")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            createAccount()
        elif choice == '2':
            depositMoney()
        elif choice == '3':
            withdrawMoney()
        elif choice == '4':
            checkBalance()
        elif choice == '5':
            transactionHistory()
        elif choice == '6':
            transferMoney()
        elif choice == '7':
            calculateInterest()
        elif choice == '8':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

                            # Main Program ------------------------
def main():
    """Entry point of the program."""
    load_data()
    creds = read_credentials()
    if adminLogin(creds):
        mainMenu()

main()