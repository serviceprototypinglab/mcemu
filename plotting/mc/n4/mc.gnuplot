set title "Monte Carlo Approximation for Selected Distributions (Fixed Omega, n=4)"
set grid lt rgb "#191970" ztics ytics xtics
set hidden3d
set surface
set xtics font ",8" offset -0.8,0.3
set ytics font ",8" offset -0.8,0.0
set ztics font ",8" offset 1.0,0.0
set xrange [0.0:0.40]
set yrange [10:100]
set zrange [-0.1:0.3]
set xlabel "epsilon"
set ylabel "trials"
set zlabel "inaccuracy"
set dgrid3d 20,18 gauss 0.01, 1
set view 50,140,0.92
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
set cbrange [-0.1:0.33]

set term pdf monochrome dashed
#set term pdf

set output "mc.pdf"
set datafile separator ","
splot 'mc4.csv' using 1:2:3 title 'k=4' with lines palette, 'mc3.csv' using 1:2:3 title 'k=3' with lines palette
