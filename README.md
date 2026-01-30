# SQA Banking App
# 🏦 Banking System Front-End Test Suite

## Assumptions
- Text-based interface
- Input via standard input
- Known test account:
  - Account: 123456
  - PIN: 4321
  - Balance: $1000

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
- Ryan Hastings
- Myron Lobo (100874243)
- Abdul Ghafour Ahmed (100929766)
- Anthony Ciceu
