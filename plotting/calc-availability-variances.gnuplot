set title "ø Data Availability (over variances)"
set grid lt rgb "#191970"
set hidden3d
set surface
set parametric
set xtics 1
set ytics 40
set ztics 0.1
set xrange [2:10]
set yrange [0.0:400.0]
set zrange [0.75:1.0]
set xlabel "services"
set ylabel "σ²"
set zlabel "ø data availability"
set style data lines
#set dgrid3d 10,11,1
set dgrid3d 9,11 gauss 1, 40
set view 60,320,0.95
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
set cbrange [0.75:1.01]

#set terminal x11
#set terminal svg
set term pdf monochrome dashed
#set term pdf

set output "calc-availability-variances.pdf"
set datafile separator ","
splot 'calc-availability.csv.variances' using 1:3:4 title 'Availability' with lines palette
