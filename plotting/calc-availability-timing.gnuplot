set title "Availability Calculation Performance"
set grid lt rgb "#191970" ztics ytics xtics
set hidden3d
set surface
set parametric
set xtics font ",8" offset -0.9,0.1
set ytics font ",8" offset -0.6,-0.1
set ztics font ",8" offset 1.0,0.0
set xrange [1:10]
set yrange [0:100]
#set zrange [0.0:10000.0]
set zrange [0.0:20000.0]
set xlabel "services"
set ylabel "ø availability"
set zlabel "time (µs)"
set style data lines
#set dgrid3d 10,11,1
#set dgrid3d 10,11,60
set dgrid3d 10,11 gauss 1, 10
set view 60,320,0.95
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
#set cbrange [0.0:10000.0]
set cbrange [0.0:20000.0]

#set terminal x11
#set terminal svg
set term pdf monochrome dashed
#set term pdf

set output "calc-availability-timing.pdf"
set datafile separator ","
splot 'calc-availability.csv.availabilities' using 1:2:5 title 'Availability Calculation' with lines palette
