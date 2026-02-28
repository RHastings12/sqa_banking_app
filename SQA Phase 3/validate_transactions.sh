#!/bin/sh

cd inputs

for i in *; do
    echo "Checking transaction outputs of test $i"

    output="../outputs/$i.atf"

    if [ -f "$output" ]; then
        diff ../outputs/$i.atf ../expected/$i.etf
    else
        echo "No transaction for test"
    fi
done