#!/bin/bash 

echo -e "Activating Virtual Environment"
source env/bin/activate
PYTHON="python3"

# 1. Scrape Data
echo -e "1. Scrape websites to collect data "
echo -e "1a. Scraping GreatSchools website for first 100 zip codes and printing sample..."
$PYTHON web_scrape_scripts/great_schools.py
echo -e
echo -e "1b. Scraping Walk Score website for first 100 zip codes and printing sample..."
$PYTHON web_scrape_scripts/walk_score.py 
echo -e
echo -e "1c. Scraping Weather Base website for first 10 zip codes and printing sample..."
$PYTHON web_scrape_scripts/weather.py

