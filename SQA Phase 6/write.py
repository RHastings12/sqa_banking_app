def write_new_current_accounts(accounts, file_path):
    """
    Writes Current Bank Accounts File with strict validation
    Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT TT
    Where TTTT is transaction count (4 digits) and TT is account plan (SP or NP)
    Total length 45 characters.
    """
    with open(file_path, 'w') as file:
        for acc in accounts:
            # Validate account number
            if not isinstance(acc['account_number'], str) or not acc['account_number'].isdigit():
                raise ValueError(f"Account number must be numeric string, got {acc['account_number']}")
            if len(acc['account_number']) > 5:
                raise ValueError(f"Account number exceeds 5 digits: {acc['account_number']}")

            # Validate name
            if len(acc['name']) > 20:
                raise ValueError(f"Account name exceeds 20 characters: {acc['name']}")

            # Validate status
            if acc['status'] not in ('A', 'D'):
                raise ValueError(f"Invalid status '{acc['status']}'. Must be 'A' or 'D'")

            # Validate balance
            if not isinstance(acc['balance'], (int, float)):
                raise ValueError(f"Balance must be numeric, got {type(acc['balance'])}")
            if acc['balance'] < 0:
                raise ValueError(f"Negative balance detected: {acc['balance']}")
            if acc['balance'] > 99999.99:
                raise ValueError(f"Balance exceeds maximum $99999.99: {acc['balance']}")

            # Validate transaction count
            if 'total_transactions' not in acc:
                acc['total_transactions'] = 0
            if not isinstance(acc['total_transactions'], int) or acc['total_transactions'] < 0:
                raise ValueError(f"Invalid transaction count: {acc['total_transactions']}")
            if acc['total_transactions'] > 9999:
                raise ValueError(f"Transaction count exceeds 9999: {acc['total_transactions']}")

            # Validate plan type
            plan = acc.get('plan', 'NP')
            if plan not in ('SP', 'NP'):
                raise ValueError(f"Invalid plan type '{plan}'. Must be SP or NP")

            # Format fields
            acc_num = acc['account_number'].zfill(5)
            name = acc['name'].ljust(20)[:20]
            status = acc['status']
            balance = f"{acc['balance']:08.2f}"
            trans_count = f"{acc['total_transactions']:04d}"
            plan_str = plan

            # Write exactly 45 characters
            file.write(f"{acc_num} {name} {status} {balance} {trans_count} {plan_str}\n")

        # END_OF_FILE marker (also 45 characters)
        eof_name = "END_OF_FILE".ljust(20)
        file.write(f"00000 {eof_name} A 00000.00 0000 NP\n")
