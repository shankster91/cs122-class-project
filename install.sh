#!/bin/bash 

PYTHON="python3"

# 1. What OS are we running on?
PLATFORM=$($python3 -c 'import platform; print(platform.system())')

echo -e "1. Checking OS Platform..."
echo -e "\t--OS=Platform=$PLATFORM"

# 2. Create Virtual environment 
echo -e "2. Creating new virtual environment..."

# Remove the env directory if it exists 
if [[ -d env ]]; then 
    echo -e "\t--Virtual Environment already exists. Deleting old one now."
    rm -rf env  
fi

$python3 -m venv env 
if [[ ! -d env ]]; then 
    echo -e "\t--Could not create virutal environment...Please make sure venv is installed"
    exit 1
fi

# 3. Install Requirements 

echo -e "3. Installing Requirements..."
if [[ -e "requirements.txt" ]]; then 
    echo -e "\t--Need to requirements.txt to install packages."
    exit 1
fi

source env/bin/activate
pip install -r requirements.txt

# 4. Install Selenium drivers 
echo -e "4. Installing Selenium Drivers..."
if [[ $PLATFORM == 'Linux' ]];  then 
    wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz 
    tar -xvf geckodriver-v0.29.0-linux64.tar.gz
    mv geckodriver env/bin/ 
fi
deactivate 
echo -e "Install is complete."

#5. Option to run data files or continue to site
echo e- "Would you like to run the data collection files or continue straight to site?"
# things in munge
# things in web_scrape_script
