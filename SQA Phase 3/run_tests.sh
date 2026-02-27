#!/bin/sh

cd inputs

for i in *; do
    echo "Running test $i"
    python ../bankingapp.py ../currentaccounts.txt ../outputs/$i.atf < $i > ../outputs/$i.out
done