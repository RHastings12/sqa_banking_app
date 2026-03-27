## 4. Test Execution Results

The test suite was executed using Python's `unittest` framework.
This report covers white-box unit testing of the Phase 4 Back End. Two methods were selected:

- **`TransactionProcessor.execute_transaction()`** : tested using **Statement Coverage**
- **`read_old_bank_accounts()`** : tested using **Decision and Loop Coverage**

Command used:
`python -m unittest "SQA Phase 5/test_phase5_backend.py" -v`

Execution summary:
- Total tests run: 14
- Passed: 13
- Failed: 0
- Errors: 0

During execution, several validation messages were printed to the console for intentionally invalid account records. These were expected outputs from the application logic and did not represent unit test failures.


### Test Case Table

| Test     | Input              | Expected          | Coverage        |
| -------- | ------------------ | ----------------- | --------------- |
| deposit  | 03 12345 200       | balance increases | deposit branch  |
| withdraw | 04 12345 150       | balance decreases | withdraw branch |
| transfer | 05 12345 54321 300 | both update       | transfer        |
| paybill  | 06 12345 100       | balance decreases | paybill         |
| end      | 00                 | returns false     | exit            |
## 2. Method 1 – Statement Coverage: `execute_transaction()`

### 2.1 Method Source (Annotated)

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

### 2.2 Statement Coverage – Test Case Table

| Test ID | Test Name                           | Input Transaction         | Statements Covered | Expected Return | Expected Side Effect                   |
|---------|-------------------------------------|---------------------------|--------------------|-----------------|----------------------------------------|
| SC-01   | `test_deposit_transaction`          | `"03 12345 200.00"`       | S1–S4, S9          | `True`          | Account 12345 balance → 1200.00        |
| SC-02   | `test_withdraw_transaction`         | `"04 12345 150.00"`       | S1–S3, S5, S9      | `True`          | Account 12345 balance → 850.00         |
| SC-03   | `test_transfer_transaction`         | `"05 12345 54321 300.00"` | S1–S3, S6, S9      | `True`          | 12345 → 700.00; 54321 → 800.00         |
| SC-04   | `test_paybill_transaction`          | `"06 12345 100.00"`       | S1–S3, S7, S9      | `True`          | Account 12345 balance → 900.00         |
| SC-05   | `test_end_of_session_transaction`   | `"00"`                    | S1–S3, S8          | `False`         | No balance change                      |

**All 9 statements are covered across the 5 test cases.**


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

### Test Results Table
| Test      | Result |
| --------- | ------ |
| all tests | PASS   |


### Failures
No failures were observed during testing.
