# madis-dumper
downloads data from the NCEP Meterological Assimilation Data Ingest System (MADIS) archive. 

extracts station ID, latitude, longitude, observation time, and station elevation data as well as weather data, which includes: temperature, dewpoint, relative humdity, pressure, wind speed, wind direction, and quality control metrics for each. writes a time series for each weather station in individual csv files. 

\*note: this thing is pretty rough at the moment, the setup only includes operability for mesonet and rwis data (METAR data fields are  defined differently in the netCDF files on the server). requires numpy, pandas, requests, and netcdf4 modules (i believe the latter requires associated C libraries and is a pain to get working properly). **this program will generate new directories in the same folder the code is in: madis/LDAD_mesonet/clean (cleaned csv files); madis/LDAD_mesonet/dl (temporary file storage); and potentially madis/LDAD_mesonet/log (for connection errors and missing data). 

in the main file, change the DateConstructor() class to the time window in question. enter the year as an integer, the month, day, and hour range in integer tuples. to obtain data within the spatial extents of Ohio in 2014 from January to March, use: DateConstructor(2014, (1, 3), (1, 31), (0, 23)) and Madis(long_ext=(-85.0, -80.6), lat_ext=(38.3, 42.4), start_time=start, iterator=dates). the day window does not wrap, so using DateConstructor(2014, (1, 3), (4, 5), (0, 23)) will only download data from January 4-5 and March 4-5. be careful when specifying windows, the netCDF files are in utc time.

the default values for DateGenerator() are June, 1 2015 at 12:00 est, corresponding to the default values of Madis() which are the spatial extents (long, lat tuples) of Ohio. 
