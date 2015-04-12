set title "Staggered Distribution Results"
set grid lt rgb "#191970" ztics
set hidden3d
set surface
set xtics font ",8" offset -0.8,0.3
set ytics font ",8" offset -0.8,0.0
set ztics font ",8" offset 1.0,0.0
set xrange [0.8:1.0]
set yrange [100:260]
set zrange [0:16]
set xlabel "min availability"
set ylabel "min capacity"
set zlabel "# results"
set dgrid3d 84,68 gauss 0.01, 1
set view 50,140,0.95
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
set cbrange [0:20]

set term pdf monochrome dashed
#set term pdf

set output "staggered.pdf"
set datafile separator ","
splot 'staggered.csv' using 1:2:3 title 'Distributions' with lines palette
