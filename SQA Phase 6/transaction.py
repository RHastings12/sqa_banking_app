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
            03 123456 200.00
            04 123456 300.00
        """
        code_map = {"DEP": "03", "WDR": "04"}
        code = code_map.get(self.trans_code, "00")
        return f"{code} {self.account_number} {self.amount:.2f}"
