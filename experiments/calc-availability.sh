#!/bin/sh

cd ..
./calc-availability.py availabilities > plotting/calc-availability.csv.availabilities
./calc-availability.py variances > plotting/calc-availability.csv.variances
