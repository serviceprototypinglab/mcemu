set title "Combination Calculation Price (PICav)"
set grid lt rgb "#191970" ztics ytics xtics
set hidden3d
set surface
set parametric
set xtics font ",8" offset -0.9,0.1
set ytics font ",8" offset -0.6,-0.1
set ztics font ",8" offset 1.0,0.0
set xrange [1:10]
set yrange [0.9:1.0]
set zrange [0.0:16.0]
set xlabel "services"
set ylabel "target availability"
set zlabel "price (-)"
set style data lines
#set dgrid3d 10,11,1
set dgrid3d 10,10 gauss 1, 0.01
set view 60,320,0.90
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
set cbrange [0.0:16.0]

#set terminal x11
#set terminal svg
set term pdf monochrome dashed
#set term pdf

set output "picav-price.pdf"
set datafile separator ","
splot 'picav.csv' using 1:2:7 title 'Price' with lines palette

# FIXME: filter out by factor before? multiple graphs, one per factor?
