+-------------------+<>-----*+-------------------+
|    BankingApp     |        |      Account      |
+-------------------+        +-------------------+
| - accounts_file   |        | - account_number  |
| - trans_file      |        | - pin             |
| - accounts        |        | - balance         |
| - current_user    |        +-------------------+
| - transactions    |        | + __init__()      |
+-------------------+        | + validate_pin()  |
| + __init__()      |        | + get_balance()   |
| + load_accounts() |        | + update_balance()|
| + write_trans()   |        +-------------------+
| + login()         |
| + logout()        |          +-------------------+
| + view_balance()  |----------> Transaction       |
| + deposit()       |          +-------------------+
| + withdraw()      |          | - trans_code      |
| + process_menu()  |          | - account_number  |
| + run()           |          | - amount          |
+-------------------+          +-------------------+
                               | + __init__()      |
                               | + format()        |
                               +-------------------+

## Class Descriptions

### BankingApp

**Core program; controls program startup, reading accounts file, writing transactions, handling login sessions, showing menus, performing banking operations, and running the main loop.**

#### Attributes

| Attribute      | Meaning                                                  |
| -------------- | -------------------------------------------------------- |
| `accounts_file`| Name of input accounts file (e.g., `"accounts.txt"`)     |
| `trans_file`   | Name of output transaction file (e.g., `"daily_transactions.txt"`) |
| `accounts`     | A list or dictionary containing `Account` objects        |
| `current_user` | The `Account` object of the currently logged‑in user     |
| `transactions` | A list of `Transaction` objects created this session     |

#### Methods

| Method            | Purpose                                                      |
| ----------------- | ------------------------------------------------------------ |
| `__init__()`      | Set filenames, load accounts, initialize variables           |
| `load_accounts()` | Read the accounts file and create `Account` objects          |
| `write_trans()`   | Write a `Transaction` object to the output file              |
| `login()`         | Ask user for account number & PIN, authenticate              |
| `logout()`        | Clear the active session                                     |
| `view_balance()`  | Print the current user’s balance                             |
| `deposit()`       | Add money to the user’s account and record the transaction   |
| `withdraw()`      | Subtract money (if sufficient funds) and record the transaction |
| `process_menu()`  | Read a command (deposit, withdraw, logout, exit, etc.)       |
| `run()`           | Main loop that starts the front‑end and keeps it running     |

**Relationship:**  
`BankingApp` <>-----* `Account` (aggregation) – BankingApp contains many Account objects.

---

### Account

**Holds everything the program knows about a user: account number, PIN, balance.**

#### Attributes

| Attribute        | Meaning                                    |
| ---------------- | ------------------------------------------ |
| `account_number` | Unique ID for the account (e.g., `"123456"`) |
| `pin`            | PIN associated with account                 |
| `balance`        | Current balance                             |

#### Methods

| Method             | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| `__init__()`       | Creates the Account object                       |
| `validate_pin()`   | Confirms PIN matches user input                  |
| `get_balance()`    | Returns balance                                  |
| `update_balance()` | Updates balance after deposit/withdraw           |

---

### Transaction

**A simple object that holds the details of a single banking transaction. Used only to store transaction data (type + account + amount) and produce a formatted line for the daily transaction file.**

#### Attributes

| Attribute        | Meaning                                      |
| ---------------- | -------------------------------------------- |
| `trans_code`     | Code for type of transaction (DEP, WDR, etc.) |
| `account_number` | The account affected                         |
| `amount`         | Amount deposited/withdrawn                    |

#### Methods

| Method       | Purpose                                            |
| ------------ | -------------------------------------------------- |
| `__init__()` | Creates a Transaction object                       |
| `format()`   | Converts entry to formatted text for output file   |

**Relationship:**  
`BankingApp` -----> `Transaction` – BankingApp creates new Transaction objects whenever the user makes a deposit or withdrawal. Other actions (login/logout/balance) do not produce transactions.
