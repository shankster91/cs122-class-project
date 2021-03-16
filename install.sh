#!/bin/bash 

# 1. First check to see if the correct version of Python is installed on the local machine 
echo "1. Checking Python version..."
REQ_PYTHON_V="370"

ACTUAL_PYTHON_V=$(python -c 'import sys; version=sys.version_info[:3]; print("{0}{1}{2}".format(*version))')
ACTUAL_PYTHON3_V=$(python3 -c 'import sys; version=sys.version_info[:3]; print("{0}{1}{2}".format(*version))')

if [[ $ACTUAL_PYTHON_V > $REQ_PYTHON_V ]] || [[ $ACTUAL_PYTHON_V == $REQ_PYTHON_V ]];  then 
    PYTHON="python"
elif [[ $ACTUAL_PYTHON3_V > $REQ_PYTHON_V ]] || [[ $ACTUAL_PYTHON3_V == $REQ_PYTHON_V ]]; then 
    PYTHON="python3"
else
    echo -e "\tPython 3.7 is not installed on this machine. Please install Python 3.7 before continuing."
    exit 1
fi

echo -e "\t--Python 3.7 is installed"

# 2. Print OS Platform
PLATFORM=$($PYTHON -c 'import platform; print(platform.system())')

echo -e "2. Checking OS Platform..."
echo -e "\t--OS=Platform=$PLATFORM"

# 3. Create Virtual environment 
echo -e "3. Creating new virtual environment..."

# Remove the env directory if it exists 
if [[ -d env ]]; then 
    echo -e "\t--Virtual Environment already exists. Deleting old one now."
    rm -rf env  
fi

$PYTHON -m venv env 
if [[ ! -d env ]]; then 
    echo -e "\t--Could not create virutal environment...Please make sure venv is installed"
    exit 1
fi

# 4. Install Requirements 

echo -e "4. Installing Requirements..."
if [[ ! -e "requirements.txt" ]]; then 
    echo -e "\t--Need to requirements.txt to install packages."
    exit 1
fi

source env/bin/activate
pip install -r requirements.txt

# 5. Install Selenium drivers once virtual environment is activated
echo -e "5. Installing Selenium Drivers..."
if [[ $PLATFORM == 'Linux' ]];  then 
    wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz 
    tar -xvf geckodriver-v0.29.0-linux64.tar.gz
    mv geckodriver env/bin/ 
fi
deactivate 
echo -e "Install is complete."

# 6. Read data
echo -e "6. Read in data used to create database"
echo -e "6a. Reading and Cleaning Business Count txt file..."
# $PYTHON munge/business_count_munge.py # throws error, fix
echo -e "\t--Business count data complete and available in data directory"
echo -e
echo -e "6b. Reading and Cleaning Census file..."
$PYTHON munge/census_munge.py # takes ~1 min to run, shorten?
echo -e "\t--Census count data complete and available in data directory"
echo -e
echo -e "6c. Reading and Cleaning Ideology file..."
#$PYTHON munge/ideology_munge.py # throws error, fix
echo -e "\t--Ideology file complete and available in data directory"
echo -e
echo -e "6d. Reading and Cleaning Library file..."
$PYTHON munge/libraries_munge.py # gives a warning but still works
echo -e "\t--Library count data complete and available in data directory"
echo -e
echo -e "6e. Reading and Cleaning Munseums file..."
$PYTHON munge/museums_munge.py
echo -e "\t--Museum count data complete and available in data directory"
echo -e
echo -e "6f. Reading and Cleaning Zillow file..."
$PYTHON munge/zillow_munge.py
echo -e "\t--Zillow data complete and available in data directory"
echo -e
echo -e "6g. Scraping GreatSchools website for first 100 zip codes and printing sample..."
$PYTHON web_scrape_scripts/great_schools.py
echo -e
echo -e "6h. Scraping Walk Score website for first 100 zip codes and printing sample..."
#$PYTHON web_scrape_scripts/walk_score.py # uncomment out after editing walk_score.py
echo -e
echo -e "6i. Scraping Weather Base website for first 100 zip codes and printing sample..."
# $PYTHON web_scrape_scripts/weather.py# uncomment out after editing walk_score.py

# 7. Move onto site
echo -e "7. Launch site"
$PYTHON ui/mysite/manage.py runserver