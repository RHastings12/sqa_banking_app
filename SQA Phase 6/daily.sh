#!/bin/sh

cd tests

for i in *; do
    python ../bankingapp.py ../currentaccounts.txt < $i
done

cd ../Transactions

# Combine session outputs into single file
cat session_*.txt > ../dailytransout.atf

python ../backend.py ../dailytransout.atf ../currentaccounts.txt ../masteraccounts.txt