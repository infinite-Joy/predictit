first the number of countries was taken

## get cricsheet data
wget http://cricsheet.org/downloads/all.zip

this should download a zip file whcih contains the yaml files and the readme.txt

Tests:
    py.test <test file>

to get the countries run:

python organise_retrieved_data.py >> countries.txt

multiple times with varying list of files

remove the unique entries

cat countries.txt | perl -ne '$H{$_}++ or print' > countries_uniq.txt

mv countries_uniq.txt countries.txt

#######################

then we need to convert city name to latitude longitude

ex: curl http://maps.googleapis.com/maps/api/geocode/json?address=London&sensor=false

python map_city_longitude_latitide.py

would give us json data with the city name and the latitude longitude info in them in that order

##################

get all numerical data


cat 913629.yaml | perl -ne 'print "$1\n" if /(\d+)/' > numerical_data.txt 

##################################

## get all overs data

python organise_retrieved_data.py > data.out

## introduce new line

sed "s/], /],\n/g" data.out > data.out_bak
mv data.out_bak data.out

## remove the parenthesis

sed "s/\],//g" data.out > data.out_bak
mv data.out_bak data.out
sed "s/\[//g" data.out > data.out_bak
mv data.out_bak data.out

# this will take the 10 % data lines in a file randomly
awk 'BEGIN {srand()} !/^$/ { if (rand() <= .1) print $0}' data.out > data_test.out

cat data.out | awk '{ print $(NF) }' > y_data.out

cat data_test.out | awk '{ print $(NF) }' > y_data_test.out

