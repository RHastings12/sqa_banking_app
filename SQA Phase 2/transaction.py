"""
Transaction class

Stores details of a single banking transaction
and formats it for output to transaction file.
"""


class Transaction:

    def __init__(self, trans_code, account_number, amount):
        """
        Creates a Transaction object.
        """
        self.trans_code = trans_code
        self.account_number = account_number
        self.amount = amount

    def format(self):
        """
        Formats transaction for writing to file.
        """
        return f"{self.trans_code} {self.account_number} {self.amount:.2f}"
