"""
Account class

Represents a single bank account.
Stores account number, PIN, and balance.
"""


class Account:

    def __init__(self, account_number, pin, balance):
        """
        Creates an Account object.
        """
        self.account_number = account_number
        self.pin = pin
        self.balance = balance

    def validate_pin(self, input_pin):
        """
        Confirms whether the PIN matches.
        """
        return self.pin == input_pin

    def get_balance(self):
        """
        Returns the current balance.
        """
        return self.balance

    def update_balance(self, amount):
        """
        Updates the account balance.
        Positive amount = deposit
        Negative amount = withdrawal
        """
        self.balance += amount
