# madis-dumper
downloads data from the NCEP Meterological Assimilation Data Ingest System (MADIS) archive. 

extracts station ID, latitude, longitude, observation time, and station elevation data as well as weather data, which includes: temperature, dewpoint, relative humdity, pressure, wind speed, wind direction, and quality control metrics for each. writes a time series for each weather station in individual csv files. 

\*note: this thing is pretty rough at the moment, the setup only includes operability for mesonet and rwis data. requires numpy, pandas, requests, and netcdf4 modules. the DateConstructor generator class needs to be retooled and integrated into the Madis class.
