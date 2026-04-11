#!/bin/sh

cd tests

for dir in */; do
    cd "$dir"

    # Run frontend for each input file
    for file in *; do
        python ../../bankingapp.py ../../currentaccounts.txt < "$file"
    done

    cd ../../Transactions

    # Combine outputs
    cat session_*.txt > ../dailytransout.atf

    # Run backend using 
    python ../backend.py ../dailytransout.atf ../currentaccounts.txt ../masteraccounts.txt

    # Reset transaction logs
    cd ../
    TRANSACTIONS_DIR="./Transactions"

    if [ -d "$TRANSACTIONS_DIR" ]; then
        echo "Cleaning $TRANSACTIONS_DIR..."
        find "$TRANSACTIONS_DIR" -mindepth 1 -delete
    else
        echo "ERROR: $TRANSACTIONS_DIR not found"
        exit 1
    fi

    # Go back to tests for next folder
    cd tests
done