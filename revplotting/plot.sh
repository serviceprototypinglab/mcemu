#!/bin/sh

for i in *.gnuplot; do echo $i; gnuplot $i; done
#cp *.pdf /home/josef/Work/repos/habil/manuscript/graphs/
