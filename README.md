## Predictor


How to use the fetch_data_script:

There are some issues with the lxml installation but other than that all other installations in virtualenv should be fine

This was done using python2.7

### Setup the environment in ubuntu

Install PYTHON3:
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.5

get pip:
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.5 get-pip.py

setup virtual env:
sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
virtualenv -p python3.5 py3_venv
source py3_venv/bin/activate
pip install Scrapy
scrapy docs can be found here
http://doc.scrapy.org/en/latest/intro/install.html

installing dependencies
pip install -r fetching_data_scripts/requirements.txt
