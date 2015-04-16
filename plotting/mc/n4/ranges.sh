#!/bin/sh
#
# Call: ranges.sh <*.csv>

max=`cut -d "," -f 3 $1 | grep -v ^- | sort -g | tail -1`
min=`cut -d "," -f 3 $1 | grep ^- | sort -g | tail -1`

echo "min $min max $max"
