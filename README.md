# SQA Banking App
# 🏦 Banking System Front-End Test Suite

## to run the app, simply go to the directory of the respective Phase and run 
```python bankingapp.py currentaccounts.txt transout.atf```

## Assumptions
- Text-based interface
- Input via standard input
- Known test account:
  - Account: 123456
  - PIN: 4321
  - Balance: $1000




# Phase 3: Front End Requirements Testing

## Project Overview

The application allows a user to:
- Log in
- View balance
- Deposit money
- Withdraw money
- Log out
- Exit the system

---

## Project Structure

```
SQA Phase 3/
├── bankingapp.py
├── account.py
├── transaction.py
├── currentaccounts.txt
├── transout.atf
├── Transactions/
│   └── history_*.txt
├── inputs/          ← test input files (one per test case)
├── expected/        ← expected .atf and .out files
└── outputs/         ← actual outputs from test runs
```

### File Descriptions

| File | Purpose |
|------|---------|
| `bankingapp.py` | Main application controller and event loop |
| `account.py` | Account class representing a single bank account |
| `transaction.py` | Transaction class for recording deposits and withdrawals |
| `currentaccounts.txt` | Input file containing account information (format: `account_number pin balance`) |
| `transout.atf` | Output file storing recorded transactions in `.atf` format |

## How to Run

### Command-Line Usage

```bash
python bankingapp.py <accounts_file> <trans_file>
```

**Examples:**
```bash
python bankingapp.py currentaccounts.txt transout.atf
```

- `accounts_file` : Plain text file listing accounts (format: `account_number pin balance`)
- `trans_file`    : Output file where daily transactions are appended in `.atf` format

If no arguments are given, defaults are `currentaccounts.txt` and `transout.atf`. All transactions are logged to the specified `.atf` file, and session history is also saved with timestamps in the `Transactions/` directory.

---
## Test Account

The system includes a known test account:

```
Account Number: 123456
PIN: 4321
Balance: 1000.00
```

This account is stored in:

```
currentaccounts.txt
```

---

## User Interface

The banking application uses a **menu-driven interface** after login:

```
Welcome to the Banking System
Enter account number:
Enter PIN:
Login successful
Main Menu:
1. View Balance
2. Deposit
3. Withdraw
4. Logout
5. Exit
```

### Menu Options (After Login)

| Option | Action | Description |
|--------|--------|-------------|
| **1** | View Balance | Display current account balance |
| **2** | Deposit | Add funds to account |
| **3** | Withdraw | Remove funds from account |
| **4** | Logout | End current session and return to login |
| **5** | Exit | Terminate the program |

---

### Accounts File

The accounts file contains a list of accounts in the format:

```
account_number pin balance
```

Example (`currentaccounts.txt`):

```
123456 4321 1000.00
```

Each line represents one account with:
- **account_number** — unique identifier (typically 6 digits)
- **pin** — numeric password (typically 4 digits)
- **balance** — initial account balance

---

## Transaction Output Format (`.atf`)

All transactions are logged to the specified `.atf` (ATM Transaction File) output file and can be viewed on any code/text viewing app:

```
DEP 123456 200.00
WDR 123456 50.00
```

Format:
```
<TRANS_CODE> <ACCOUNT_NUMBER> <AMOUNT>
```

Where:
- **TRANS_CODE** — `DEP` (deposit) or `WDR` (withdrawal)
- **ACCOUNT_NUMBER** — The account that performed the transaction
- **AMOUNT** — The transaction amount (formatted to 2 decimal places)

### Session History Logging

In addition to the `.atf` file, each session creates a timestamped history log in the `Transactions/` directory:

```
Transactions/history_YYYYMMDD_HHMMSS.txt
```

This log records all session events:
- LOGIN events
- LOGOUT events  
- DEP (deposit) transactions
- WDR (withdrawal) transactions

---

---

## Architecture

The system follows the UML Design we created that is in this github as well:

- `BankingApp`  
  Controls program execution, session handling, and user commands.

- `Account`  
  Stores account number, PIN, and balance.

- `Transaction`  
  Stores transaction details and formats output for file writing.

Relationships:
- BankingApp aggregates multiple Account objects.
- BankingApp creates Transaction objects during deposit/withdraw operations.

## Known Constraints

- Only one account is pre-loaded in `accounts.txt` by default (`123456 / PIN 4321 / $1000.00`)
- Balances are stored in memory during a session; the accounts file is **not** updated on disk
- The `.atf` transaction file is **appended to** on each run (never overwritten)
- On EOF (end of redirected input), the program exits cleanly


---



## 📋 Test Case Table

| Test ID/Valid/Invalid/Edge | Test Name | What the Test Is Intended to Verify |
|---------|-----------|--------------------------------------|
| **TC-01**/V | Valid Login | Verifies that a user can successfully log in using valid credentials |
| **TC-02**/I | Invalid Login | Verifies that the system rejects incorrect login credentials |
| **TC-03**/V | Logout | Verifies that a logged-in user can log out successfully |
| **TC-04**/V | Exit Program | Verifies clean program exit from main menu |
| **TC-05**/V | View Balance | Verifies correct display of account balance |
| **TC-06**/V | Deposit Valid Amount | Verifies valid deposit updates balance correctly |
| **TC-07**/E | Deposit Zero Amount | Verifies system rejects zero deposit |
| **TC-08**/E | Deposit Negative Amount | Verifies system rejects negative deposit |
| **TC-09**/V | Withdraw Valid Amount | Verifies valid withdrawal processes correctly |
| **TC-10**/V | Withdraw Exact Balance | Verifies withdrawing entire balance results in zero |
| **TC-11**/I | Withdraw Excess Amount | Verifies system prevents overdraft |
| **TC-12**/E | Withdraw Zero Amount | Verifies zero withdrawal is rejected |
| **TC-13**/E | Withdraw Negative Amount | Verifies negative withdrawal is rejected |
| **TC-14**/I | Invalid Menu Option | Verifies error handling for invalid menu choice |
| **TC-15**/I | Invalid Command Format | Verifies malformed commands don't crash system |
| **TC-16**/I | Operation Without Login | Verifies operations require authentication |
| **TC-17**/E | Recovery After Error | Verifies system continues after invalid input |
| **TC-18**/E | Exit After Error | Verifies clean exit even after errors |
| **TC-19**/V | End Session Properly | Verifies proper session termination |
| **TC-20**/I | Login While Logged In | Prevents duplicate login state |

## 👥 Contributors
- Ryan Hastings (100894215)
- Myron Lobo (100874243)
- Abdul Ghafour Ahmed (100929766)
- Anthony Ciceu (100787198)
