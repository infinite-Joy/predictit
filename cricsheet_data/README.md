## model description
to get the prediction if the batsman is going to be out in the next ball

## get cricsheet data
wget http://cricsheet.org/downloads/all.zip

this should download a zip file whcih contains the yaml files and the readme.txt

## Testing

This works in both py.test and nosetests framework
(py3_venv_deepL_conda)vagrant@precise32:~/predictor/predictor/cricsheet_data$ py.test -v
========================================================================= test session starts ==========================================================================
platform linux -- Python 3.5.2, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /home/vagrant/.conda/envs/py3_venv_deepL_conda/bin/python
cachedir: .cache
rootdir: /home/vagrant/predictor/predictor/cricsheet_data, inifile:
collected 15 items

tests/test_map_city_longitude_latitide.py::test_get_cities PASSED
tests/test_map_city_longitude_latitide.py::test_get_lat_lon_from PASSED
tests/test_map_city_longitude_latitide.py::test_query_google_vincent PASSED
tests/test_organise_retrieved_data.py::test_get_all_matches_yaml_list PASSED
tests/test_organise_retrieved_data.py::test_read_file_in_zip PASSED
tests/test_organise_retrieved_data.py::test_read_file_in_zip_readme PASSED
tests/test_organise_retrieved_data.py::test_read_file_in_zip2 PASSED
tests/test_organise_retrieved_data.py::test_get_all_over PASSED
tests/test_organise_retrieved_data.py::test_give_delivery_info PASSED
tests/test_organise_retrieved_data.py::test_give_delivery_info_wicket PASSED
tests/test_organise_retrieved_data.py::test_handle_ind_innings PASSED
tests/test_xdata_ydata_partII.py::test_get_relevant_data_date PASSED
tests/test_xdata_ydata_partII.py::test_get_relevant_data_float PASSED
tests/test_xdata_ydata_partII.py::test_get_relevant_data_num PASSED
tests/test_xdata_ydata_partII.py::test_get_lat_lng PASSED

====================================================================== 15 passed in 5.77 seconds =======================================================================
(py3_venv_deepL_conda)vagrant@precise32:~/predictor/predictor/cricsheet_data$ nosetests
...............
----------------------------------------------------------------------
Ran 15 tests in 5.699s

OK


## to get the countries run:

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

## did a very silly mistake
see
(py3_venv_deepL_conda)vagrant@precise32:~/predictor/predictor/cricsheet_data$ sed -n '792239p' data.out
53.8007554 -1.5490774 32.6 0 0 0 130 013.193887 -59.543198 0.1 0 0 0 0

so put new lines whereever there is ]]

## format of data.out
please ensure the data.out to be in the following format
(py3_venv_deepL_conda)vagrant@precise32:~/predictor/predictor/cricsheet_data$ tail -10 data.out
-9.443800399999999 147.1802671 46.2 4 0 4 220 0
-9.443800399999999 147.1802671 46.3 1 0 1 221 0
-9.443800399999999 147.1802671 46.4 2 0 2 223 0
-9.443800399999999 147.1802671 46.5 2 0 2 225 0
-9.443800399999999 147.1802671 46.6 0 0 0 225 1
-9.443800399999999 147.1802671 47.1 2 0 2 227 0
-9.443800399999999 147.1802671 47.2 0 0 0 227 1
-9.443800399999999 147.1802671 47.3 0 1 1 228 0
-9.443800399999999 147.1802671 47.4 0 0 0 228 1
-9.443800399999999 147.1802671 47.5 0 0 0 228 1


# this will take the 10% data lines in a file randomly
awk 'BEGIN {srand()} !/^$/ { if (rand() <= .1) print $0}' data.out > data_test.out

cat data.out | awk '{ print $(NF) }' > y_data.out

cat data_test.out | awk '{ print $(NF) }' > y_data_test.out

## remove the last digit(y part) from data.out and data_test.out

sed "s/\w*$//" data.out > data.out_bak
mv data.out_bak data.out

sed "s/\w*$//" data_test.out > data_test.out_bak
mv data_test.out_bak data_test.out

## for some reason max_features as multiples of 5 are only working

so changes this according to that

## things to do next
next get the datasets of all the files. 
run into into the model
and then generate the model and save it to a h5py file

also work on the logging part
