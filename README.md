# madis-dumper
downloads data from the NCEP Meterological Assimilation Data Ingest System (MADIS) archive. 

extracts station ID, latitude, longitude, observation time, and station elevation data as well as weather data, which includes: temperature, dewpoint, relative humdity, pressure, wind speed, wind direction, and quality control metrics for each. writes a time series for each weather station in individual csv files. 

\*note: this thing is pretty rough at the moment, the setup only includes operability for mesonet and rwis data. requires numpy, pandas, requests, and netcdf4 modules. the DateConstructor generator class needs to be retooled and integrated into the Madis class, currently only accepts 24 hour windows. 

in the main file, change the DateConstructor() class to the time window in question. enter the year, month range in a tuple, and the day range in a tuple. the default for hour is zero, but this is subject to change. so to obtain data within the spatial extents of Ohio in 2014 from January to March, use: DateConstructor(2014, (1, 3), (1, 31), 0) and Madis(long_ext=(), lat_ext=(), start_time=start, iterator=dates). the day window does not wrap, so using DateConstructor(2014, (1, 3), (4, 5), 0) will only download data from January 1-3 and March 4-5.
