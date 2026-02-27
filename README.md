# SQA Banking App
# 🏦 Banking System Front-End Test Suite

## to run the app, simply go to the directory of the respective Phase and run 
```python bankingapp.py currentaccounts.txt dailytransout.atf```

## Assumptions
- Text-based interface
- Input via standard input
- Known test account:
  - Account: 123456
  - PIN: 4321
  - Balance: $1000




# CSCI 3060U – Phase 3: Front End Requirements Testing

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
├── accounts.txt
├── dailytransout.atf
├── Transactions/
│   └── history_*.txt
├── inputs/          ← test input files (one per test case)
├── expected/        ← expected .atf and .out files
└── outputs/         ← actual outputs from test runs
```

### File Descriptions

| File | Purpose |
|------|---------|
| `banking_app.py` | Main application controller and program loop |
| `account.py` | Account class definition |
| `transaction.py` | Transaction class definition |
| `accounts.txt` | Input file containing account information |
| `daily_transactions.txt` | Output file storing recorded transactions |


## How to Run

### Command-Line Usage

```bash
python bankingapp.py <accounts_file> <trans_file>
```

**Examples:**
```bash
python bankingapp.py accounts.txt dailytransout.atf
```

- `accounts_file` — Plain text file listing accounts (format: `account_number pin balance`)
- `trans_file`    — Output file where daily transactions are appended in `.atf` format

If no arguments are given, defaults are `accounts.txt` and transaction history is going to be saved in the `Transaction` directory.

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
accounts.txt
```

---

## Available Commands

When running, the program will prompt:

```
Enter command (login, logout, balance, deposit, withdraw, exit):
```

### Commands

| Command | Description |
|----------|-------------|
| `login` | Log into an account |
| `logout` | Log out of current session |
| `balance` | View account balance |
| `deposit` | Deposit money |
| `withdraw` | Withdraw money |
| `exit` | Exit the program |

---

## Input File Format

`accounts.txt` format:

```
account_number pin balance
```

Example:

```
123456 4321 1000.00
```

---

## Output File

All deposit and withdrawal transactions are written to:

```
daily_transactions.txt
```

Transaction format:

```
<TRANS_CODE> <ACCOUNT_NUMBER> <AMOUNT>
```

Example:

```
DEP 123456 200.00
WDR 123456 50.00
```

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
