#set term pdf monochrome dashed
set term pdf enhanced lw 3 size 5.00in,3.00in
set termoption dash

set style data boxes
set style fill solid 1.0

set output "trace-singleservice.pdf"
set datafile separator ","

set multiplot layout 2,1 title "Emulation of Service Unavailability on Scenario 'singleservice'"
#set title "Emulation of Service Unavailability on Scenario 'singleservice'"
set yrange[-0.05:1.35]
set ytics 0,1
#set xrange[0:10000]

set xlabel "Time (s)" textcolor rgbcolor "white"
set ylabel "Unavailability (true/false)" offset 0,-5
plot 'singleservice.convergence.csv' using 1:2 title 'anyservice/0.9/convergence' lt 1 lc rgb '#c0c0c0'
set xlabel "Time (s)" textcolor rgbcolor "black"
set ylabel " "
plot 'singleservice.incident.csv' using 1:2 title 'anyservice/0.9/incident' lt 1 lc rgb '#c0c0c0'
