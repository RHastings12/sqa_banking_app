"""
Backend Banking System

Processes daily transaction files and updates the current accounts file.

Input Files:
    currentaccounts.txt
    dailytransout.atf

Output Files:
    newaccounts.txt

Run with:
    python backend.py
"""

from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error


class AccountManager:
    """
    Handles all account related operations.
    """

    def __init__(self, accounts):
        self.accounts = accounts

    def find_account(self, account_number):
        for acc in self.accounts:
            if acc["account_number"] == account_number:
                return acc
        return None

    def deposit(self, account_number, amount):
        acc = self.find_account(account_number)

        if acc:
            acc["balance"] += amount
        else:
            log_constraint_error("Account not found", "DEPOSIT")

    def withdraw(self, account_number, amount):
        acc = self.find_account(account_number)

        if acc:
            acc["balance"] -= amount
        else:
            log_constraint_error("Account not found", "WITHDRAW")

    def transfer(self, from_account, to_account, amount):
        acc1 = self.find_account(from_account)
        acc2 = self.find_account(to_account)

        if acc1 and acc2:
            acc1["balance"] -= amount
            acc2["balance"] += amount
        else:
            log_constraint_error("Transfer account missing", "TRANSFER")

    def pay_bill(self, account_number, amount):
        acc = self.find_account(account_number)

        if acc:
            acc["balance"] -= amount
        else:
            log_constraint_error("Account not found", "PAYBILL")


class TransactionProcessor:
    """
    Reads and executes transactions.
    """

    def __init__(self, account_manager):
        self.account_manager = account_manager

    def read_transactions(self, file_path):
        with open(file_path) as f:
            return [line.strip() for line in f]

    def execute_transaction(self, transaction):

        parts = transaction.split()
        code = parts[0]

        if code == "03":  # deposit
            self.account_manager.deposit(parts[1], float(parts[2]))

        elif code == "04":  # withdraw
            self.account_manager.withdraw(parts[1], float(parts[2]))

        elif code == "05":  # transfer
            self.account_manager.transfer(parts[1], parts[2], float(parts[3]))

        elif code == "06":  # paybill
            self.account_manager.pay_bill(parts[1], float(parts[2]))

        elif code == "00":  # end of session
            return False

        return True


class BankingBackend:
    """
    Main backend controller.
    """

    def __init__(self):
        self.accounts = []

    def load_accounts(self):
        self.accounts = read_old_bank_accounts("currentaccounts.txt")

    def process_transactions(self):
        manager = AccountManager(self.accounts)
        processor = TransactionProcessor(manager)

        transactions = processor.read_transactions("dailytransout.atf")

        for t in transactions:
            if not processor.execute_transaction(t):
                break

    def save_accounts(self):
        write_new_current_accounts(self.accounts, "newaccounts.txt")

    def run(self):
        self.load_accounts()
        self.process_transactions()
        self.save_accounts()


if __name__ == "__main__":
    backend = BankingBackend()
    backend.run()