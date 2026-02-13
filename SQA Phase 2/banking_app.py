"""
BankingApp - SQA Banking System Front-End

Core Responsibilities:
- Program startup
- Reading accounts file
- Writing transactions
- Handling login session
- Showing menus
- Performing banking operations
- Running the main loop

Input:
    - accounts file (e.g., accounts.txt)
    - user commands via standard input

Output:
    - standard output (responses)
    - daily transaction file (e.g., daily_transactions.txt)
"""

from account import Account
from transaction import Transaction


class BankingApp:
    """
    Core program class that controls system execution.
    """

    def __init__(self, accounts_file, trans_file):
        """
        Initializes system variables and loads accounts.
        """
        self.accounts_file = accounts_file
        self.trans_file = trans_file
        self.accounts = {}
        self.current_user = None
        self.transactions = []

        self.load_accounts()

    def load_accounts(self):
        """
        Reads the accounts file and creates Account objects.
        Expected format per line:
        account_number pin balance
        """
        try:
            with open(self.accounts_file, "r") as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        acc_num, pin, balance = parts
                        self.accounts[acc_num] = Account(
                            acc_num, pin, float(balance)
                        )
        except FileNotFoundError:
            print("Accounts file not found.")

    def write_trans(self, transaction):
        """
        Writes a Transaction object to the output transaction file.
        """
        with open(self.trans_file, "a") as file:
            file.write(transaction.format() + "\n")

    def login(self):
        """
        Authenticates user based on account number and PIN.
        """
        if self.current_user is not None:
            print("Already logged in.")
            return

        acc_num = input("Account Number: ")
        pin = input("PIN: ")

        account = self.accounts.get(acc_num)

        if account and account.validate_pin(pin):
            self.current_user = account
            print("Login successful.")
        else:
            print("Invalid login credentials.")

    def logout(self):
        """
        Ends the current session.
        """
        if self.current_user is None:
            print("No user logged in.")
        else:
            self.current_user = None
            print("Logged out successfully.")

    def view_balance(self):
        """
        Displays current user's balance.
        """
        if self.current_user is None:
            print("Please login first.")
            return

        print(f"Current balance: ${self.current_user.get_balance():.2f}")

    def deposit(self):
        """
        Adds money to account and records transaction.
        """
        if self.current_user is None:
            print("Please login first.")
            return

        try:
            amount = float(input("Deposit amount: "))
        except ValueError:
            print("Invalid amount.")
            return

        if amount <= 0:
            print("Invalid deposit amount.")
            return

        self.current_user.update_balance(amount)

        transaction = Transaction("DEP",
                                  self.current_user.account_number,
                                  amount)

        self.transactions.append(transaction)
        self.write_trans(transaction)

        print("Deposit successful.")

    def withdraw(self):
        """
        Withdraws money if sufficient funds exist.
        """
        if self.current_user is None:
            print("Please login first.")
            return

        try:
            amount = float(input("Withdraw amount: "))
        except ValueError:
            print("Invalid amount.")
            return

        if amount <= 0:
            print("Invalid withdrawal amount.")
            return

        if self.current_user.get_balance() < amount:
            print("Insufficient funds.")
            return

        self.current_user.update_balance(-amount)

        transaction = Transaction("WDR",
                                  self.current_user.account_number,
                                  amount)

        self.transactions.append(transaction)
        self.write_trans(transaction)

        print("Withdrawal successful.")

    def process_menu(self):
        """
        Reads a user command and executes the corresponding action.
        """
        command = input("Enter command (login, logout, balance, deposit, withdraw, exit): ")

        if command == "login":
            self.login()
        elif command == "logout":
            self.logout()
        elif command == "balance":
            self.view_balance()
        elif command == "deposit":
            self.deposit()
        elif command == "withdraw":
            self.withdraw()
        elif command == "exit":
            return False
        else:
            print("Invalid menu option.")

        return True

    def run(self):
        """
        Main loop of the application.
        """
        running = True
        while running:
            running = self.process_menu()

        print("Exiting system.")


if __name__ == "__main__":
    app = BankingApp("accounts.txt", "daily_transactions.txt")
    app.run()
