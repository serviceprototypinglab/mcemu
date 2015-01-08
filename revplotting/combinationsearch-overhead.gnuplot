set title "Combination Calculation Overhead"
set grid lt rgb "#191970"
set hidden3d
set surface
set parametric
set xtics 1
set ytics 0.01
set ztics 0.5
set xrange [1:10]
set yrange [0.9:1.0]
set zrange [0.0:2.0]
set xlabel "services"
set ylabel "target availability"
set zlabel "overhead (%)"
set style data lines
#set dgrid3d 10,11,1
set dgrid3d 10,10 gauss 1, 0.01
set view 60,320,0.95
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
set cbrange [0.0:2.0]

#set terminal x11
#set terminal svg
set term pdf monochrome dashed
#set term pdf

set output "combinationsearch-overhead.pdf"
set datafile separator ","
splot 'combinationsearch.csv' using 1:2:5 title 'Overhead' with lines palette
