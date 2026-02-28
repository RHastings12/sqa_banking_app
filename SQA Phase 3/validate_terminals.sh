#!/bin/sh

cd inputs

for i in *; do
    echo "Checking terminal outputs of test $i"
    diff ../outputs/$i.out ../expected/$i.eout
done