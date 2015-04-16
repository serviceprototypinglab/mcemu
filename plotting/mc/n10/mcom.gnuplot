set title "Monte Carlo Approximation for Selected Distributions (Fixed Trials, n=10)"
set grid lt rgb "#191970" ztics
set hidden3d
set surface
set xtics font ",8" offset -0.8,0.3
set ytics font ",8" offset -0.8,0.0
set ztics font ",8" offset 1.0,0.0
set xrange [0.0:0.40]
set yrange [0:1024]
set zrange [-0.2:1.0]
set xlabel "epsilon"
set ylabel "omega"
set zlabel "inaccuracy"
set dgrid3d 20,206 gauss 0.01, 1
set view 50,140,0.92
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
set cbrange [0:20]

set term pdf monochrome dashed
#set term pdf

set output "mcom.pdf"
set datafile separator ","
splot 'mc10om.csv' using 1:2:3 title 'k=10' with lines palette, 'mc9om.csv' using 1:2:3 title 'k=9' with lines palette
