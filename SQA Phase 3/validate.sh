#!/bin/sh

cd inputs

for i in *; do
    echo "Checking outputs of test $i"
    diff ../outputs/$i.out ../expected/$i.etf
done