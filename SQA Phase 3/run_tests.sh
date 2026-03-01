#!/bin/sh

cd inputs

# Create outputs folder if it doesn't exist
mkdir -p "../outputs"

for i in *; do
    echo "Running test $i"
    python ../bankingapp.py ../currentaccounts.txt ../outputs/$i.atf < $i > ../outputs/$i.out
done