#/usr/bin/env bash

while read p; do
	program=$(echo $p | awk '{ print($1) }')
	version=$(echo $p | awk '{ print($2) }')
	echo $p
	echo Adequate
	/usr/bin/python3 py/experimentAdequate.py line $program $version 50
	echo Budget
	/usr/bin/python3 py/experimentBudget.py line $program $version 1
done <programs.txt
