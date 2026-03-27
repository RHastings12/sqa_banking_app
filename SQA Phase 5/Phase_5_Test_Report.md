## 4. Test Execution Results

The test suite was executed using Python's `unittest` framework.
This report covers white-box unit testing using the Phase 4 files. Two methods were selected:

- **`TransactionProcessor.execute_transaction()`** : tested using **Statement Coverage**
- **`read_old_bank_accounts()`** : tested using **Decision and Loop Coverage**

Command used:
`python -m unittest "SQA Phase 5/test_phase5_backend.py" -v`

Execution summary:
- Total tests run: 14
- Passed: 14
- Failed: 0
- Errors: 2 (fixed)

During execution, several validation messages were printed to the console for intentionally invalid account records (e.g., `ERROR: Fatal error - Line 1: Account number must be 5 digits`). These were expected outputs from the application's validation logic and did not represent unit test failures, the two actual failures are documented in Section **7**.


## Method 1 : Statement Coverage: `execute_transaction()` 

### 4.1 Method Source (from the backend.py file from Phase 4)

```python
def execute_transaction(self, transaction):         # S1
    parts = transaction.split()                     # S2
    code = parts[0]                                 # S3

    if code == "03":                                # D1
        self.account_manager.deposit(...)           # S4
    elif code == "04":                              # D2
        self.account_manager.withdraw(...)          # S5
    elif code == "05":                              # D3
        self.account_manager.transfer(...)          # S6
    elif code == "06":                              # D4
        self.account_manager.pay_bill(...)          # S7
    elif code == "00":                              # D5
        return False                                # S8

    return True                                     # S9
```

**Statements to cover:** S1–S9  
**Decisions to exercise:** D1–D5 (each taken True once)

### 4.2. Statement Coverage

| Test ID | Test Name                           | Input Transaction         | Statements Covered | Expected Return | Expected Side Effect                   |
|---------|-------------------------------------|---------------------------|--------------------|-----------------|----------------------------------------|
| SC-01   | `test_deposit_transaction`          | `"03 12345 200.00"`       | S1–S4, S9          | `True`          | Account 12345 balance → 1200.00        |
| SC-02   | `test_withdraw_transaction`         | `"04 12345 150.00"`       | S1–S3, S5, S9      | `True`          | Account 12345 balance → 850.00         |
| SC-03   | `test_transfer_transaction`         | `"05 12345 54321 300.00"` | S1–S3, S6, S9      | `True`          | 12345 → 700.00; 54321 → 800.00         |
| SC-04   | `test_paybill_transaction`          | `"06 12345 100.00"`       | S1–S3, S7, S9      | `True`          | Account 12345 balance → 900.00         |
| SC-05   | `test_end_of_session_transaction`   | `"00"`                    | S1–S3, S8          | `False`         | No balance change                      |

**All 9 statements are covered across the 5 test cases.**

---

### Decision + Loop Table

| Test                 | Case              | Expected      |
| -------------------- | ----------------- | ------------- |
| valid                | correct format    | account added |
| invalid length       | wrong length      | rejected      |
| invalid account      | letters in ID     | rejected      |
| invalid status       | not A/D           | rejected      |
| invalid balance      | negative          | rejected      |
| invalid transactions | not digits        | rejected      |
| invalid plan         | not SP/NP         | rejected      |
| multiple lines       | mix valid/invalid | loop works    |

---

## 5. Method 2 : Decision and Loop Coverage: `read_old_bank_accounts()`

### 5.1 Method Structure (Annotated)

```
accounts = []                                               # Init
open file
  for each line in file:                                    # LOOP L1
      clean_line = line.rstrip('\n')

      if len(clean_line) != 45: continue                   # D1 : length check

      try:
          extract fields (account_number, name, status,
                          balance_str, transactions_str, plan_type)

          if not account_number.isdigit(): continue         # D2 : account number
          if status not in ('A', 'D'): continue            # D3 : status
          if balance_str[0] == '-': continue               # D4 : negative sign check
          if (malformed balance format): continue          # D5 : balance format
          if not transactions_str.isdigit(): continue      # D6 : transaction count
          if plan_type not in ('SP', 'NP'): continue       # D7 : plan type

          balance = float(balance_str)
          transactions = int(transactions_str)

          if balance < 0: continue                         # D8 : business rule balance
          if transactions < 0: continue                    # D9 : business rule transactions

          accounts.append({...})                           # Append valid account

      except Exception: continue                           # D10 : exception handler

return accounts
```

**Decisions:** D1–D10  
**Loop L1:** must be tested at zero iterations, one iteration, and multiple iterations.

---

### 5.2 Decision and Loop Coverage : Test Case Table

| Test ID | Test Name                           | Loop Iterations | Decisions Exercised                              | Input Description                              | Expected # Accounts |
|---------|-------------------------------------|-----------------|--------------------------------------------------|------------------------------------------------|---------------------|
| DL-01   | `test_valid_single_account`         | 1               | D1=F, D2=F, D3=F, D4=F, D5=F, D6=F, D7=F       | Valid 45-char line, all fields correct         | 1                   |
| DL-02   | `test_invalid_length_line`          | 1               | D1=T                                             | Line is 32 chars (not 45)                      | 0                   |
| DL-03   | `test_invalid_account_number`       | 1               | D1=F, D2=T                                       | Account number `0A234` (contains letter)       | 0                   |
| DL-04   | `test_invalid_status`               | 1               | D1=F, D2=F, D3=T                                 | Status field is `X` (not A or D)              | 0                   |
| DL-05   | `test_negative_balance_format`      | 1               | D1=F, D2=F, D3=F, D4=T                           | Balance starts with `-`                        | 0                   |
| DL-06   | `test_invalid_transaction_count`    | 1               | D1=F, D2=F, D3=F, D4=F, D5=F, D6=T              | Transaction count is `00A0` (contains letter)  | 0                   |
| DL-07   | `test_invalid_plan_type`            | 1               | D1=F, D2=F, D3=F, D4=F, D5=F, D6=F, D7=T        | Plan type is `XX` (not SP or NP)               | 0                   |
| DL-08   | `test_multiple_lines_loop_coverage` | 3               | L1 multiple; D2=T on line 3                      | 2 valid lines + 1 invalid account number       | 2                   |
| DL-09   | `test_empty_file_zero_iteration`    | 0               | L1 = 0 (loop body never executes)                | Empty file                                     | 0                   |

**Loop coverage:** DL-09 covers zero iterations; DL-01 through DL-07 cover one iteration; DL-08 covers multiple iterations including a mid-loop rejection.

---

## 6. Individual Test Results Table

### Statement Coverage : `execute_transaction()`

| Test ID | Test Method Name                        | Input                     | Expected Return | Expected Balance Change                | Result  |
|---------|-----------------------------------------|---------------------------|-----------------|----------------------------------------|---------|
| SC-01   | `test_deposit_transaction`              | `"03 12345 200.00"`       | `True`          | 12345: 1000.00 → **1200.00**           | ✅ PASS |
| SC-02   | `test_withdraw_transaction`             | `"04 12345 150.00"`       | `True`          | 12345: 1000.00 → **850.00**            | ✅ PASS |
| SC-03   | `test_transfer_transaction`             | `"05 12345 54321 300.00"` | `True`          | 12345 → **700.00**; 54321 → **800.00** | ✅ PASS |
| SC-04   | `test_paybill_transaction`              | `"06 12345 100.00"`       | `True`          | 12345: 1000.00 → **900.00**            | ✅ PASS |
| SC-05   | `test_end_of_session_transaction`       | `"00"`                    | `False`         | No change                              | ✅ PASS |

### Decision and Loop Coverage : `read_old_bank_accounts()`

| Test ID | Test Method Name                          | Input Description                         | Expected # Accounts | Actual # Accounts | Result  |
|---------|------------------------------------------|-------------------------------------------|---------------------|-------------------|---------|
| DL-01   | `test_valid_single_account`              | Valid 45-char line, all fields correct    | 1                   | 1                 | ❌ FAIL |
| DL-02   | `test_invalid_length_line`               | Line too short (32 chars, not 45)         | 0                   | 0                 | ✅ PASS |
| DL-03   | `test_invalid_account_number`            | Account number `0A234` (non-digit)        | 0                   | 0                 | ✅ PASS |
| DL-04   | `test_invalid_status`                    | Status `X` (not A or D)                  | 0                   | 0                 | ✅ PASS |
| DL-05   | `test_negative_balance_format`           | Balance starts with `-`                   | 0                   | 0                 | ✅ PASS |
| DL-06   | `test_invalid_transaction_count`         | Transaction count `00A0` (non-digit)      | 0                   | 0                 | ✅ PASS |
| DL-07   | `test_invalid_plan_type`                 | Plan type `XX` (not SP or NP)             | 0                   | 0                 | ✅ PASS |
| DL-08   | `test_multiple_lines_loop_coverage`      | 3 lines: 2 valid, 1 invalid account #    | 2                   | 2                 | ❌ FAIL |
| DL-09   | `test_empty_file_zero_iteration`         | Empty file                                | 0                   | 0                 | ✅ PASS |

---

## 7. Failures

**2 failures in one bug were uncovered by testing.**

---

### BUG-01 : Leading Zeros Stripped from Account Numbers

| Field            | Detail |
|------------------|--------|
| **Bug ID**       | BUG-01 |
| **Severity**     | Medium |
| **Affects**      | `read_old_bank_accounts()` in `read.py` (line 70) in phase 4 |
| **Tests Failed** | DL-01 (`test_valid_single_account`), DL-08 (`test_multiple_lines_loop_coverage`) |

**Description:**  
When a valid account is appended to the list, the account number is stored using `account_number.lstrip('0')`. This silently strips all leading zeros from the raw 5-digit field. For example, the input `"01234"` is stored as `"1234"`.

**Root Cause (`read.py` line 70):**
```python
# Actual code (buggy)
'account_number': account_number.lstrip('0') or '0',

# Expected behaviour
'account_number': account_number,
```

**Failure Output (from test run):**
```
FAIL: test_valid_single_account
AssertionError: '1234' != '01234'

FAIL: test_multiple_lines_loop_coverage
AssertionError: '1234' != '01234'
```

**Impact:**  
Any downstream code (e.g., `find_account()` in `backend.py`) that looks up an account using the original 5-digit number as it appears in a transaction file will fail to find accounts with leading zeros. This causes deposit, withdraw, transfer, and paybill operations to silently do nothing for those accounts, producing incorrect balances in the output file without any error being raised.

**Fix:** Remove the `lstrip('0')` call and store the account number exactly as read from the file. If lookup without leading zeros is needed elsewhere, normalisation should be applied consistently to both stored values and all lookup inputs.


### Failures
No failures were observed after fixing the 2 failures detected above.
