#!/bin/bash 

# 1. Set Python variable
echo -e "1. Check Python Version"
PYTHON="python3"

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
pip3 install -r requirements.txt

# 5. Install Selenium drivers once virtual environment is activated
echo -e "5. Installing Selenium Drivers..."
if [[ $PLATFORM == 'Linux' ]];  then 
    wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz 
    tar -xvf geckodriver-v0.29.0-linux64.tar.gz
    mv geckodriver env/bin/ 
fi
echo -e "Install is complete."

# 6. Read data
echo -e "6. Read in data used to create database"
echo -e
echo -e "6a. Reading and Cleaning Business Count txt file..."
$PYTHON munge/business_count_munge.py
echo -e "\t--Business count data complete and available in data directory"
echo -e
echo -e "6b. Reading and Cleaning Census file (note: takes about one minute to run)..."
$PYTHON munge/census_munge.py 
echo -e "\t--Census count data complete and available in data directory"
echo -e
echo -e "6c. Reading and Cleaning Ideology file..."
$PYTHON munge/ideology_munge.py
echo -e "\t--Ideology file complete and available in data directory"
echo -e
echo -e "6d. Reading and Cleaning Library file..."
$PYTHON -W"ignore" munge/libraries_munge.py
echo -e "\t--Library count data complete and available in data directory"
echo -e
echo -e "6e. Reading and Cleaning Museums file..."
$PYTHON munge/museums_munge.py
echo -e "\t--Museum count data complete and available in data directory"
echo -e
echo -e "6f. Reading and Cleaning Zillow file..."
$PYTHON munge/zillow_munge.py
echo -e "\t--Zillow data complete and available in data directory"

# 7. load algorithm arguments
echo -e
echo -e "7. Load variable counts for similarity algorithm"
$PYTHON algorithm/get_counts.py
echo -e

# 8. Move onto site
echo -e "8. Launch site"
$PYTHON ui/mysite/manage.py runserver


