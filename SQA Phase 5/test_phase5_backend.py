import os
import sys
import tempfile
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PHASE4_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "SQA Phase 4"))

if PHASE4_DIR not in sys.path:
    sys.path.insert(0, PHASE4_DIR)

from backend import AccountManager, TransactionProcessor
from read import read_old_bank_accounts


class TestExecuteTransactionStatementCoverage(unittest.TestCase):
    """
    Statement coverage tests for TransactionProcessor.execute_transaction()
    """

    def setUp(self):
        self.accounts = [
            {
                "account_number": "12345",
                "name": "John Doe",
                "status": "A",
                "balance": 1000.00,
                "total_transactions": 0,
                "plan": "NP"
            },
            {
                "account_number": "54321",
                "name": "Jane Doe",
                "status": "A",
                "balance": 500.00,
                "total_transactions": 0,
                "plan": "SP"
            }
        ]
        self.manager = AccountManager(self.accounts)
        self.processor = TransactionProcessor(self.manager)

    def test_deposit_transaction(self):
        result = self.processor.execute_transaction("03 12345 200.00")
        self.assertTrue(result)
        self.assertEqual(self.accounts[0]["balance"], 1200.00)

    def test_withdraw_transaction(self):
        result = self.processor.execute_transaction("04 12345 150.00")
        self.assertTrue(result)
        self.assertEqual(self.accounts[0]["balance"], 850.00)

    def test_transfer_transaction(self):
        result = self.processor.execute_transaction("05 12345 54321 300.00")
        self.assertTrue(result)
        self.assertEqual(self.accounts[0]["balance"], 700.00)
        self.assertEqual(self.accounts[1]["balance"], 800.00)

    def test_paybill_transaction(self):
        result = self.processor.execute_transaction("06 12345 100.00")
        self.assertTrue(result)
        self.assertEqual(self.accounts[0]["balance"], 900.00)

    def test_end_of_session_transaction(self):
        result = self.processor.execute_transaction("00")
        self.assertFalse(result)


class TestReadOldBankAccountsDecisionLoopCoverage(unittest.TestCase):
    """
    Decision and loop coverage tests for read_old_bank_accounts()
    """

    def create_temp_file(self, lines):
        temp = tempfile.NamedTemporaryFile(mode="w", delete=False, newline="\n")
        temp.write("\n".join(lines))
        temp.close()
        return temp.name

    def test_valid_single_account(self):
        lines = [
            "01234 John Doe             A 01000.00 0000 NP"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]["account_number"], "1234")
        self.assertEqual(accounts[0]["name"], "John Doe")
        self.assertEqual(accounts[0]["status"], "A")
        self.assertEqual(accounts[0]["balance"], 1000.00)
        self.assertEqual(accounts[0]["total_transactions"], 0)
        self.assertEqual(accounts[0]["plan"], "NP")

    def test_invalid_length_line(self):
        lines = [
            "01234 John Doe A 1000.00 0000 NP"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 0)

    def test_invalid_account_number(self):
        lines = [
            "0A234 John Doe             A 01000.00 0000 NP"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 0)

    def test_invalid_status(self):
        lines = [
            "01234 John Doe             X 01000.00 0000 NP"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 0)

    def test_negative_balance_format(self):
        lines = [
            "01234 John Doe             A -1000.00 0000 NP"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 0)

    def test_invalid_transaction_count(self):
        lines = [
            "01234 John Doe             A 01000.00 00A0 NP"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 0)

    def test_invalid_plan_type(self):
        lines = [
            "01234 John Doe             A 01000.00 0000 XX"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 0)

    def test_multiple_lines_loop_coverage(self):
        lines = [
            "01234 John Doe             A 01000.00 0000 NP",
            "02345 Sarah Smith          A 00500.00 0000 NP",
            "0A345 Invalid User         A 00300.00 0000 NP"
        ]
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 2)
        self.assertEqual(accounts[0]["account_number"], "1234")
        self.assertEqual(accounts[1]["account_number"], "2345")

    def test_empty_file_zero_iteration(self):
        lines = []
        file_path = self.create_temp_file(lines)

        accounts = read_old_bank_accounts(file_path)

        os.remove(file_path)

        self.assertEqual(len(accounts), 0)

if __name__ == "__main__":
    unittest.main()
