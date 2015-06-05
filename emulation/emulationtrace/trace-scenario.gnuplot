#set term pdf monochrome dashed
set term pdf enhanced lw 3 size 5.00in,3.00in
set termoption dash

set style data boxes
set style fill solid 1.0

set output "trace-scenario.pdf"
set datafile separator ","

set multiplot layout 3,1 title "Emulation of Service Unavailability on Scenario 'scenario'"
set yrange[-0.05:1.05]
set ytics 0,1
#set xrange[0:10000]

set format x ""
set ylabel " "
plot 'scenario.csv' using 1:2 title 'A/0.3' lt 1 lc rgb '#c00000'
set ylabel "Availability (true/false)"
plot 'scenario.csv' using 1:3 title 'B/0.4' lt 1 lc rgb '#c000c0'
set ylabel " "
set xlabel "Time (s)"
set format x "%g"
plot 'scenario.csv' using 1:4 title 'C/0.5' lt 1 lc rgb '#c0c000'
