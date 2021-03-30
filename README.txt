INSTRUCTIONS FOR RUNNING THE APPLICATION

1.	Open a terminal and navigate to project directory.
2.  Get a Google Maps API key here: https://developers.google.com/maps/documentation/javascript/get-api-key
    Place this API Key in line 12 of ui/mysite/zipsearch/views.py and save.
3.	Run:
    chmod 775 install.sh
4.	To launch the application, type:
	./install.sh 
5.	Open a web browser and navigate to http://127.0.0.1:8000/.
6.	In the zip code field, type in a starting zip code.
7.	Use the drop-down menu to choose the target state.
8.	Check any combination of boxes corresponding to preferences. At least one box must be checked.
9.	Click “Submit”
10.	Wait patiently while the results populate.
11.	Read the results and have fun interacting with the map!
12.	(optional) To run a sample of the web scraping process, type:
	./run_scraping.sh
