#!/bin/sh

cd inputs

for i in *; do
    echo "Checking transaction outputs of test $i"

    # Only attempt to validate if the file exists
    if [ -f "../outputs/$i.atf" ]; then
        diff ../outputs/$i.atf ../expected/$i.etf
    else
        echo "No transaction"
    fi
done