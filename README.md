# GUS8066 Redistricting Project 2023

## This application conducts common redistricting tests on redistricting plans in .csv format. 

### Quickstart
Clone the repository. You only need the files in the top level of the repository's directory, as well as the data folder. (The docs folder contains files to create documentation).

Make sure you downloaded the file, 'requirements.txt'. In your console, run the following code ''pip install -r requirements.txt''. This will create the necessary virtual environment to run the GUI.

### Using the GUI

Step 1. Run the executable or gui.py from the top level of the repository.

Step 2. Select the path to the folder containing the plans. Two plans have been provided for testing. They are located in /data.

Step 3. Select a shapefile or geopackage if desired (one has been supplied in /data: vtd_gdf.gpkg.)

Step 4. Select the census geography type for download.

Step 5. Choose the population column from the user supplied shapefile or geopackage (here, tot_pop.)

Step 6. Select historical election data if partisan fairness tests are desired. Two ZIP files have been included in this package.
           HOUSE and SENATE precinct general.zip unzip to over 100 MB each and include electoral outcomes by local voting district.
	   They must be unzipped to a local folder. The zip files are located in /data/elections.
		
Step 7. Choose your tests. Only choose tests if you have supplied the neccessary information, eg. Do not select partisan fairness
	    tests if you have not chosen a path to historical election data. 
		
Step 8. Press button to score plans.

Step 9. A file ('score.csv') will be written to a folder named 'output' in the local directory. 

		
		
