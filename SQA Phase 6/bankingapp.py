"""
bankingapp.py  —  Banking ATM Front End
==================================================
Command-line usage:
    
    python bankingapp.py currentaccounts.txt

stdin  → user keystrokes (or redirected test input file)
stdout → terminal log (what the user sees on screen)
<trans_file> → daily transaction file  (appended to, never overwritten)
               defaults to  daily_transactions.txt  if not given
"""

import sys
import os
from pathlib import Path

from account import Account
from transaction import Transaction
from read import read_bank_accounts

# Required for encoding some characters
if sys.platform.startswith("win"):
    # Python 3.7+
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ══════════════════════════════════════════════════════════════════════════════
# CLI formatting helpers  
# ══════════════════════════════════════════════════════════════════════════════

_W = 46          # inner width of every box row

def _box_top() -> str:  return "╔" + "═" * _W + "╗"
def _box_bot() -> str:  return "╚" + "═" * _W + "╝"
def _box_div() -> str:  return "╠" + "═" * _W + "╣"

def _box_row(txt: str, align: str = "left") -> str:
    if align == "center": padded = txt.center(_W)
    elif align == "right": padded = txt.rjust(_W)
    else: padded = txt.ljust(_W)
    return "║" + padded + "║"

def _banner() -> None:
    print(_box_top())
    print(_box_row("  Banking App Terminal", "left"))
    print(_box_row("  Phase 6", "left"))
    print(_box_div())
    print(_box_row("  Welcome to the Banking System", "left"))
    print(_box_bot())

def _menu_box(account_number: str) -> None:
    print(_box_top())
    print(_box_row(f"  Account: {account_number}", "left"))
    print(_box_div())
    print(_box_row("  Main Menu:", "left"))
    print(_box_row("", "left"))
    print(_box_row("    1.  View Balance", "left"))
    print(_box_row("    2.  Deposit", "left"))
    print(_box_row("    3.  Withdraw", "left"))
    print(_box_row("    4.  Transfer", "left"))
    print(_box_row("    5.  Logout", "left"))
    print(_box_row("    6.  Exit", "left"))
    print(_box_bot())

def _section(title: str) -> None:
    print("┌─ " + title + " " + "─" * max(0, _W - len(title) - 3) + "┐")

def _section_end() -> None:
    print("└" + "─" * _W + "┘")

def _ok(msg: str)   -> None: print(f"  ✔  {msg}")
def _err(msg: str)  -> None: print(f"  ✖  {msg}")
def _info(msg: str) -> None: print(f"  ℹ  {msg}")

def _bal(amount: int) -> None:
    bar_max  = 30
    fraction = min(amount / 5000, 1.0) if amount > 0 else 0
    filled   = int(fraction * bar_max)
    bar      = "█" * filled + "░" * (bar_max - filled)
    print(f"  Balance  │{bar}│  ${amount:,}")


def _prompt(label: str) -> str:
    """Styled input prompt. Returns empty string on EOF (automated test runs)."""
    try:
        print(f"  ▶  {label}: ")
        return input().strip()
    except EOFError:
        return ""


# ══════════════════════════════════════════════════════════════════════════════
# BankingApp  
# ══════════════════════════════════════════════════════════════════════════════

class BankingApp:
    """
    Main ATM application class.

    UML attributes
    --------------
    - accounts_file : str
    - trans_file    : str
    - accounts      : dict[str, Account]   ← aggregates many Account objects
    - current_user  : Account | None
    - history_dir   : str                   ← directory where session histories are kept
    - history_file  : str                   ← current run's history log file
    """

    # ── __init__ ──────────────────────────────────────────────────────── #
    def __init__(self, accounts_file: str) -> None:
        self.accounts_file: str                = accounts_file
        self.accounts:      dict[str, Account] = {}
        self.current_user:  Account | None     = None

        # prepare history logging
        # history files are stored inside a "Transactions" subfolder of
        # the application directory (phase 3 folder). we create the
        # directory if it doesn't exist and open a fresh log for each run.
        self.history_dir: str = os.path.join(os.path.dirname(__file__), "Transactions")
        os.makedirs(self.history_dir, exist_ok=True)
        
        base_dir = Path(__file__).parent
        transactions_dir = base_dir / "Transactions"
        file_count = sum(1 for f in transactions_dir.iterdir() if f.is_file())

        self.history_file: str = os.path.join(self.history_dir, f"session_{file_count + 1}.txt")

        # load the accounts after history is ready.
        self.load_accounts()

    # ── load_accounts ─────────────────────────────────────────────────── #
    def load_accounts(self) -> None:
        """Read <accounts_file> and populate self.accounts dict."""
        with open(self.accounts_file, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 7:
                    continue          # skip malformed lines silently
                acc_num, name, pin, bal = parts[0].lstrip('0'), f"{parts[1]} {parts[2]}", parts[5], parts[4]
                try:
                    balance = float(bal)
                except ValueError:
                    continue
                self.accounts[acc_num] = Account(acc_num, name, pin, balance)

    # ── write_trans ───────────────────────────────────────────────────── #
    def write_trans(self, transaction: Transaction) -> None:
        """
        Append transaction record to the history log for current session

        Format (both files):  <CODE> <ACCOUNT_NUMBER> <AMOUNT>  (same as
        Transaction.format()).
        """
        record = transaction.format() + "\n"

        # record in history as well
        self.log_history(record.strip())

    def log_history(self, line: str) -> None:
        """Write an arbitrary line to the current history file.

        The argument *line* should **not** contain a terminating newline; this
        method will add one automatically.  Errors are swallowed to keep the
        ATM running even if disk issues occur.
        """
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(str(line) + "\n")
        except Exception:
            pass

    # ── login ─────────────────────────────────────────────────────────── #
    def login(self) -> bool:
        """Prompt for credentials. Returns True on success, False on failure."""
        _banner()
        print()
        _section("Login")
        account_number = _prompt("Account number")
        if not account_number:
            return False

        pin = _prompt("PIN          ")
        _section_end()

        acc = self.accounts.get(account_number)
        if acc is None or not acc.validate_credentials(account_number, pin):
            _err("Invalid credentials")
            return False

        self.current_user = acc
        _ok("Login successful")
        print()
        return True

    # ── logout ────────────────────────────────────────────────────────── #
    def logout(self) -> None:
        """End the current session."""
        self.current_user = None
        _ok("Logout successful")
        print()

    # ── view_balance ──────────────────────────────────────────────────── #
    def view_balance(self) -> None:
        """Print the current balance with a visual progress bar."""
        if self.current_user is None:
            return
        _section("Balance")
        _bal(int(self.current_user.get_balance()))
        _section_end()
        print()

    # ── deposit ───────────────────────────────────────────────────────── #
    def deposit(self) -> None:
        """
        Prompt for deposit amount, validate, update balance, and write
        a DEP record to session history log via write_trans().
        """
        if self.current_user is None:
            return
        _section("Deposit")
        raw = _prompt("Amount ($)  ")
        _section_end()

        try:
            amount = float(raw)
        except ValueError:
            _err("Invalid deposit amount")
            print()
            return

        if amount <= 0:
            _err("Invalid deposit amount")
            print()
            return

        self.current_user.update_balance(amount)
        self.write_trans(Transaction("DEP", self.current_user.account_number, amount))
        _ok(f"Deposit successful  (+${amount:,.2f})")
        _bal(int(self.current_user.get_balance()))
        print()

    # ── withdraw ──────────────────────────────────────────────────────── #
    def withdraw(self) -> None:
        """
        Prompt for withdrawal amount, validate, update balance, and write
        a WDR record to session history log via write_trans().
        """
        if self.current_user is None:
            return
        _section("Withdraw")
        raw = _prompt("Amount ($)  ")
        _section_end()

        try:
            amount = float(raw)
        except ValueError:
            _err("Invalid withdrawal amount")
            print()
            return

        if amount <= 0:
            _err("Invalid withdrawal amount")
            print()
            return

        if amount > self.current_user.get_balance():
            _err("Insufficient funds")
            print()
            return

        self.current_user.update_balance(-amount)
        self.write_trans(Transaction("WDR", self.current_user.account_number, amount))
        _ok(f"Withdrawal successful  (-${amount:,.2f})")
        _bal(int(self.current_user.get_balance()))
        print()
    
    # ── transfer ──────────────────────────────────────────────────────── #
    def transfer(self) -> None:
        if self.current_user is None:
            return
        _section("Transfer")
        raw = _prompt("Amount ($)  ")
        target_user = _prompt("Send To  ").strip().upper()
        _section_end()

        try:
            amount = float(raw)
        except ValueError:
            _err("Invalid transfer amount")
            print()
            return

        if amount <= 0:
            _err("Invalid transfer amount")
            print()
            return

        if amount > self.current_user.get_balance():
            _err("Insufficient funds")
            print()
            return
        
        target_account_number = None
        for account in self.accounts.values():
            if account.get_name().upper() == target_user:
                target_account_number = account.account_number

        if not target_account_number:
            _err("Target not found")
            print()
            return 

        self.current_user.update_balance(-amount)
        self.write_trans(Transaction("TRN", self.current_user.account_number, amount, account_target = target_account_number))
        _ok(f"Transfer successful  (-${amount:,.2f})")
        _bal(int(self.current_user.get_balance()))
        print()

    # ── process_menu ──────────────────────────────────────────────────── #
    def process_menu(self, choice: str) -> str:
        """
        Validate a raw menu-choice string and return an action token.

        Returns
        -------
        'balance'        → call view_balance()
        'deposit'        → call deposit()
        'withdraw'       → call withdraw()
        'transfer'       → call transfer()
        'logout'         → call logout(), restart outer login loop
        'exit'           → end the program
        'invalid_format' → non-integer input; print error and exit
        'invalid_option' → integer but not 1-5; show error, re-prompt
        """
        try:
            n = int(choice)
        except ValueError:
            return "invalid_format"

        return {
            1: "balance",
            2: "deposit",
            3: "withdraw",
            4: "transfer",
            5: "logout",
            6: "exit",
        }.get(n, "invalid_option")

    # ── run ───────────────────────────────────────────────────────────── #
    def run(self) -> None:
        """
        Main event loop.

        Outer while → re-prompts login after every logout.
        Inner while → reads menu input, calls process_menu(),
                      dispatches to the matching method.
        """
        #abs_path = os.path.abspath(self.trans_file)
        #_info(f"Transaction log: {abs_path}")
        #hist_path = os.path.abspath(self.history_file)
        #_info(f"History log:     {hist_path}")
        #print()

        while True:
            if not self.login():
                return

            while True:
                assert self.current_user is not None
                _menu_box(self.current_user.account_number)

                try:
                    print("  ▶  Select (1-6): ")
                    choice = input().strip()
                except EOFError:
                    return          # clean exit when input file is exhausted

                action = self.process_menu(choice)

                if action == "balance":
                    self.view_balance()

                elif action == "deposit":
                    self.deposit()

                elif action == "withdraw":
                    self.withdraw()
                
                elif action == "transfer":
                    self.transfer()

                elif action == "logout":
                    self.logout()
                    break           # back to outer loop → re-login

                elif action == "exit":
                    _info("Thank you for using the Banking System")
                    print()
                    print("  Goodbye")
                    return

                elif action == "invalid_format":
                    _err("Invalid input format")
                    print()
                    print("  Goodbye")
                    return

                else:               # invalid_option
                    _err("Invalid menu option")
                    print()


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

DEFAULT_ACCOUNTS = "currentaccounts.txt"

def main(argv: list[str]) -> int:
    """
    Usage (all forms accepted):
        python bankingapp.py                                    → defaults
        python bankingapp.py currentaccounts.txt                → custom accounts
        bank-atm currentaccounts.txt                            → via launcher
    """
    if len(argv) > 3:
        print("Usage:  bank-atm [accounts_file]")
        print(f"       bank-atm {DEFAULT_ACCOUNTS}")
        return 1

    accounts_file = argv[1] if len(argv) > 1 else DEFAULT_ACCOUNTS

    try:
        app = BankingApp(accounts_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
