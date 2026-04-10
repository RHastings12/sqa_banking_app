"""
Account
-------
Represents a single bank account.

UML Attributes:
    - account_number : str
    - pin            : str
    - balance        : float

UML Methods:
    + __init__()
    + validate_pin()
    + get_balance()
    + update_balance()
"""


class Account:
    """A single bank account with number, PIN and balance."""

    def __init__(self, account_number: str, pin: str, balance: float) -> None:
        self._account_number: str   = account_number
        self._pin:            str   = pin
        self._balance:        float = float(balance)

    # ------------------------------------------------------------------ #
    # Public read-only property so other classes can read account_number  #
    # without being able to overwrite it accidentally.                    #
    # ------------------------------------------------------------------ #
    @property
    def account_number(self) -> str:
        return self._account_number

    def validate_pin(self, input_pin: str) -> bool:
        """Return True if input_pin matches this account's PIN."""
        return self._pin == input_pin

    def validate_credentials(self, account_number: str, pin: str) -> bool:
        """Return True when both account number AND pin match."""
        return self._account_number == account_number and self._pin == pin

    def get_balance(self) -> float:
        """Return the current account balance."""
        return self._balance

    def update_balance(self, delta: float) -> None:
        """Add delta to the balance (positive = deposit, negative = withdraw)."""
        self._balance += float(delta)
