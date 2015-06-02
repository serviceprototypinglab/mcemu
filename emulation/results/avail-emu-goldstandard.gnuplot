#set term pdf monochrome dashed
set term pdf enhanced lw 3
set termoption dash

set title "Emulation of Data Availability on Scenario 'goldstandard'"
set ylabel "Availability (%)"
set xlabel "Time (s)"

set style data lines

set output "avail-emu-goldstandard.pdf"
set datafile separator ","

set key right bottom

plot 0.90 title 'target' lt 1 lc rgb '#000000' lw 3, 0.98 notitle lt 3 lc rgb '#c00000', 'goldstandard/combinatory.csv' title 'combinatory' lt 1 lc rgb '#c00000', 0.9986 notitle lt 3 lc rgb '#c000c0', 'goldstandard/picav.csv' title 'picav' lt 1 lc rgb '#c000c0', 0.99 notitle lt 3 lc rgb '#c0c000', 'goldstandard/absolute.csv' title 'absolute' lt 1 lc rgb '#c0c000', 0.9702 notitle lt 3 lc rgb '#0000c0', 'goldstandard/picav+.csv' title 'picav+' lt 1 lc rgb '#0000c0', 0.93 notitle lt 3 lc rgb '#30c030', 'goldstandard/proportional.csv' title 'proportional' lt 1 lc rgb '#30c030'

# 'goldstandard/random.csv' title 'random' lt 5
# 'goldstandard/fixed_replication.csv' title 'fixed' lt 7 => skipped because it's completely 1.0
