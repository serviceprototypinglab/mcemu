set title "Staggered Distribution Results"
set grid lt rgb "#191970"
set hidden3d
set surface
set parametric
set xtics 21
set ytics 17
set ztics 17
set xrange [0.8:1.0]
set yrange [100:260]
set zrange [0:16]
set xlabel "min availability"
set ylabel "min capacity"
set zlabel "# results"
set style data lines
set dgrid3d 21,17,1
#set dgrid3d 10,11,60
#set dgrid3d 10,11 gauss 1, 10
set view 60,320,0.95
set palette defined ( 0 '#006400',\
                      1 '#D7DF01',\
                      2 '#DF0101')
set cbrange [0:20]

#set terminal x11
#set terminal svg
set term pdf monochrome dashed
#set term pdf

set output "staggered.pdf"
set datafile separator ","
splot 'staggered.csv' using 1:2:3 title 'Staggered distributions' with lines palette
