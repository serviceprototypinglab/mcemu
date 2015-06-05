#set term pdf monochrome dashed
set term pdf enhanced lw 3 size 5.00in,5.00in
set termoption dash

set style data boxes
set style fill solid 1.0

set output "trace-picav.pdf"
set datafile separator ","

set multiplot layout 5,1 title "Emulation of Service Unavailability on Scenario 'picav'"
set yrange[-0.05:1.05]
set ytics 0,1
#set xrange[0:10000]

set format x ""
set ylabel " "
plot 'picav.csv' using 1:2 title 'Google Drive/0.99900' lt 1 lc rgb '#c00000'
plot 'picav.csv' using 1:3 title 'Amazon S3/0.98860' lt 1 lc rgb '#c000c0'
set ylabel "Availability (true/false)"
plot 'picav.csv' using 1:4 title 'AT&T/0.99500' lt 1 lc rgb '#c0c000'
set ylabel " "
plot 'picav.csv' using 1:5 title 'Linode/0.99951' lt 1 lc rgb '#c0c000'
set xlabel "Time (s)"
set format x "%g"
plot 'picav.csv' using 1:6 title 'Apple iCloud/0.99650' lt 1 lc rgb '#c0c000'
