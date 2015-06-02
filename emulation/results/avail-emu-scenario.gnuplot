#set term pdf monochrome dashed
set term pdf enhanced lw 3
set termoption dash

set title "Emulation of Data Availability on Scenario 'scenario'"
set ylabel "Availability (%)"
set xlabel "Time (s)"

set style data lines

set output "avail-emu-scenario.pdf"
set datafile separator ","

#set key right center spacing 0.9
set key at 2400,0.5

plot 0.60 title 'target' lt 1 lc rgb '#000000' lw 3, 0.79 notitle lt 3 lc rgb '#c00000', 'scenario/combinatory.csv' title 'combinatory' lt 1 lc rgb '#c00000', 0.70 notitle lt 3 lc rgb '#c000c0', 'scenario/picav.csv' title 'picav' lt 1 lc rgb '#c000c0', 0.06 notitle lt 3 lc rgb '#c0c000', 'scenario/random.csv' title 'random' lt 1 lc rgb '#c0c000'
