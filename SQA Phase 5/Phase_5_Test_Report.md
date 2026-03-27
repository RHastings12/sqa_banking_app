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
