set term pdf monochrome dashed
#set term pdf enhanced

set title "Distribution Determination Performance"
set ylabel "Runtime (s)"
set xlabel "# services"

set style data lines

set output "sweetspotservices.pdf"
set datafile separator ","
plot 'sweetspotservices.csv' using 1:2 title 'staggered-combinatoric/a=0', '' using 1:3 title 'picav+/a=0', '' using 1:4 title 'staggered-combinatoric/a=0.999', '' using 1:5 title 'picav+/a=0.999'
