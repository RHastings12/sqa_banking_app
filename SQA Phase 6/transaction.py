"""
Transaction
-----------
Stores details of a single banking transaction and formats it for the
daily transaction file (.atf).

UML Attributes:
    - trans_code     : str
    - account_number : str
    - amount         : float

UML Methods:
    + __init__()
    + format()
"""


class Transaction:
    """One deposit or withdrawal record written to the .atf file."""

    def __init__(self, trans_code: str, account_number: str, amount: float, account_target = None) -> None:
        self.trans_code:     str   = trans_code
        self.account_number: str   = account_number
        self.amount:         float = float(amount)

        self.account_target = account_target

    def format(self) -> str:
        """Return the formatted transaction string for the .atf file."""

        if self.account_target:
            return f"{self.trans_code} {self.account_number} {self.amount:.2f} {self.account_target}"

        return f"{self.trans_code} {self.account_number} {self.amount:.2f}"
