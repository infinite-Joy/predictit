# this will take the 10 % data lines in a file randomly
awk 'BEGIN {srand()} !/^$/ { if (rand() <= .1) print $0}' data.out > data_test.out

cat data.out | awk '{ print $(NF) }' > y_data.out

cat data_test.out | awk '{ print $(NF) }' > y_data_test.out
