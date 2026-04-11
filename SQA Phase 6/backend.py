"""
Backend Banking System

Processes daily transaction files and updates the current accounts file.

Input Files:
    dailytransout.atf
    currentaccounts.txt

Output Files:
    masteraccounts.txt

Run with:
    python backend.py [dailytransout.atf] [currentaccounts.txt] [masteraccounts.txt]
"""

import sys
from read import read_old_bank_accounts
from write import write_new_accounts
from print_error import log_constraint_error


class AccountManager:
    """
    Handles all account related operations.
    """

    def __init__(self, accounts):
        self.accounts = accounts

    def find_account(self, account_number):
        for acc in self.accounts:
            print(f"{account_number}   {acc["account_number"]}")
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

        if code == "DEP":  # deposit
            self.account_manager.deposit(parts[1].lstrip('0'), float(parts[2]))
        elif code == "WDR":  # withdraw
            self.account_manager.withdraw(parts[1].lstrip('0'), float(parts[2]))
        elif code == "TRNS":  # transfer
            self.account_manager.transfer(parts[1].lstrip('0'), parts[2].lstrip('0'), float(parts[3]))
        elif code == "PAY":  # paybill
            self.account_manager.pay_bill(parts[1].lstrip('0'), float(parts[2]))
        elif code == "END":  # end of session
            return False
        return True


class BankingBackend:
    """
    Main backend controller.
    """

    def __init__(self, trans_file, current_accounts_file, master_accounts_file):
        self.trans_file = trans_file
        self.current_accounts_file = current_accounts_file
        self.master_accounts_file = master_accounts_file
        self.accounts = []

    def load_accounts(self):
        self.accounts = read_old_bank_accounts(self.master_accounts_file)

    def process_transactions(self):
        manager = AccountManager(self.accounts)
        processor = TransactionProcessor(manager)
        transactions = processor.read_transactions(self.trans_file)
        for t in transactions:
            if not processor.execute_transaction(t):
                break

    def save_accounts(self):
        write_new_accounts(self.accounts, self.current_accounts_file)
        write_new_accounts(self.accounts, self.master_accounts_file)

    def run(self):
        self.load_accounts()
        self.process_transactions()
        self.save_accounts()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python backend.py <daily_transactions_file> <current_accounts_file> <master_accounts_file>")
        sys.exit(1)
    backend = BankingBackend(sys.argv[1], sys.argv[2], sys.argv[3])
    backend.run()
