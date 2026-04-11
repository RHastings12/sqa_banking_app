#!/bin/sh

cd tests/day_1

# Run all session inputs for frontend
for i in *; do
    python ../../bankingapp.py ../../currentaccounts.txt < $i
done

cd ../../Transactions

# Combine session outputs into single file
cat session_*.txt > ../dailytransout.atf

# Run backend
python ../backend.py ../dailytransout.atf ../currentaccounts.txt ../masteraccounts.txt