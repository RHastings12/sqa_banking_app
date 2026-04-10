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

    def __init__(self, trans_code: str, account_number: str, amount: float) -> None:
        self.trans_code:     str   = trans_code
        self.account_number: str   = account_number
        self.amount:         float = float(amount)

    def format(self) -> str:
        """Return the formatted transaction string for the .atf file.

        Example output:
            DEP 123456 200.00
            WDR 123456 300.00
        """
        return f"{self.trans_code} {self.account_number} {self.amount:.2f}"
