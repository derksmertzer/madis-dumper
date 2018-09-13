import requests
import gzip
import os
import logging
from inspect import currentframe
from time import time, sleep
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from netCDF4 import Dataset

from const import *


class Madis:

    def __init__(self, long_ext, lat_ext, start_time, iterator):

        self.west = long_ext[0]
        self.east = long_ext[1]
        self.south = lat_ext[0]
        self.north = lat_ext[1]
        self.start = start_time
        self.iter = iterator

    @staticmethod
    def diagnostics(*items):

        """ CALLED by date_construct, get_files(), parse_files(): diagnostics() logs the following information:
        1.) files with no information for the time period 2/3.) https server connection issues and the last file during the
        interrupt and program termination 4.) checks on the day_generator() to ensure the correct month type is applied. """

        if not os.path.exists(LOG):
            os.makedirs(LOG)

        logging.basicConfig(filename=LOG + 'diagnostics.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        func = currentframe().f_back.f_code
        # passed diagnostics from parse_files()
        if func.co_name == 'parse_files':
            logging.info('from function: {0}, no data in file {1}'.format(func.co_name, items))
        # passed diagnostics from get_files()
        if func.co_name == 'get_files' and len(items) == 1:
            logging.info('from function: {0}, no file or corrupt file {1} on https server'.format(func.co_name, items))
        if func.co_name == 'get files' and len(items) == 3:
            logging.info('from function: {0}, connection error ({1}) on file {2}'.format(func.co_name, items[1], items[0]))
        if func.co_name == 'get files' and len(items) == 2:
            logging.info('from function: {0}, program terminated at file {1} due to connection issues with '
                         'server'.format(func.co_name, items[0]))
        # passed diagnostics from date_construct()
        if func.co_name == 'date_construct':
            logging.info('from function: {0}, month type for: {1} is: {2}'.format(func.co_name, items[1], items[0]))

    def extents(self, latitude, longitude):

        """ CALLED by parse_files(): extents() returns an index mask corresponding to a specified
        spatial extent. """

        a = np.where(np.logical_and(longitude[:] < self.east, longitude[:] > self.west))
        b = np.where(np.logical_and(latitude[:] < self.north, latitude[:] > self.south))

        # check if more matching longitude values
        if a[0].shape != (0,) and b[0].shape != (0,) and a[0].shape > b[0].shape:
            print("...more matching longitude values: size = {}".format(a[0].shape))
            msk = a[0][np.isin(a[0], b[0])]
            print('...the number of returned observations within the specified spatial extent (lat: {0} - {1} ; long: '
                  '{2} - {3}) is: {4}'.format(self.south, self.north, self.west, self.east, len(msk)))
            return msk

        # check if more matching latitude values
        elif a[0].shape != (0,) and b[0].shape != (0,) and a[0].shape < b[0].shape:
            print("...more matching latitude values: size = {}".format(b[0].shape))
            msk = b[0][np.isin(b[0], a[0])]
            print('...the number of returned observations within the specified spatial extent (lat: {0} - {1} ; long: '
                  '{2} - {3}) is: {4}'.format(self.south, self.north, self.west, self.east, len(msk)))
            return msk

        # no matching stations
        else:
            print("...no matching values for file: check lat: {0} check long: {1}\n".format(b[0].shape, a[0].shape))
            return None

    @staticmethod
    def extract_station(sta_id, unique_stations, *args):

        """ CALLED by parse_files(): extract_station() masks the input station ID variable by a unique station ID variable,
        returning indices of matching records from all observations at each unique station (since this function is iterated
        over for each unique station). masks each input weather parameter packaged in *args by this record index. returns
        a packaged weather matrix of each weather observation at each station. """

        sta = np.where(sta_id[:] == unique_stations)
        pack = np.array([args[i][sta] for i in range(len(args))])
        return pack

    @staticmethod
    def append_coordinates(*args, op_flag=False):

        """ OPTIONALLY CALLED by parse_files(): append_coordinates() appends coordinate attribute information to target
        variables in the currently loaded netCDF file. this functionality is best suited for writing data to new netCDF
        files where speed is not a concern. appending to netCDF objects is time intensive. good for data destined to live
        in ArcGIS, bad for writing to over 8736 netCDF files for a yearly period. """

        if op_flag:
            for i in args:
                i.coordinates = 'timeObs latitude longitude elevation'

    def parse_files(self):

        """ CALLED by get_files(): parse_files() is the main body for cleaning files and writing the station data to
        new CSV files. """

        start2 = time()
        # loop through all netCDF files in the pointer directory
        for file in os.listdir(DL_DIR):

            print('cleaning file: {}'.format(file))
            load_time = time()
            # create an netCDF4 Dataset instance
            with Dataset(DL_DIR + file, 'a', diskless=True) as netcdf:

                # define stationID
                stationID = netcdf.variables['stationId']

                # define coordinate data
                latitude = netcdf.variables['latitude']
                longitude = netcdf.variables['longitude']
                timeObs = netcdf.variables['observationTime']
                elevation = netcdf.variables['elevation']

                # define variable data
                temp = netcdf.variables['temperature']
                dew = netcdf.variables['dewpoint']
                rh = netcdf.variables['relHumidity']
                press = netcdf.variables['stationPressure']
                winSp = netcdf.variables['windSpeed']
                winDir = netcdf.variables['windDir']

                # define QC data
                tempDD = netcdf.variables['temperatureDD']
                tempQCA = netcdf.variables['temperatureQCA']
                tempQCR = netcdf.variables['temperatureQCR']
                dewDD = netcdf.variables['dewpointDD']
                dewQCA = netcdf.variables['dewpointQCA']
                dewQCR = netcdf.variables['dewpointQCR']
                rhDD = netcdf.variables['relHumidityDD']
                rhQCA = netcdf.variables['relHumidityQCA']
                rhQCR = netcdf.variables['relHumidityQCR']
                pressDD = netcdf.variables['stationPressureDD']
                pressQCA = netcdf.variables['stationPressureQCA']
                pressQCR = netcdf.variables['stationPressureQCR']
                winSpDD = netcdf.variables['windSpeedDD']
                winSpQCA = netcdf.variables['windSpeedQCA']
                winSpQCR = netcdf.variables['windSpeedQCR']
                winDirDD = netcdf.variables['windDirDD']
                winDirQCA = netcdf.variables['windDirQCA']
                winDirQCR = netcdf.variables['windDirQCR']

                # uncomment next line if you want to append coordinate data to values
                # append_coordinates(temp, dew, rh, press, winSp, winDir,  op_flag=False)

                # global attribute which specifies point data
                netcdf.featureType = "point"

                # allows for parsing of the stationIDs
                stationID._Encoding = 'ascii'

                # pack variables into a tuple
                variables = (stationID, latitude, longitude, timeObs, temp, tempDD, tempQCA, tempQCR, dew, dewDD, dewQCA,
                             dewQCR, rh, rhDD, rhQCA, rhQCR, press, pressDD, pressQCA, pressQCR, winSp, winSpDD, winSpQCA,
                             winSpQCR, winDir, winDirDD, winDirQCA, winDirQCR, elevation)
                # dynamically extract name attribute of each variable
                names = [variables[i].name for i in range(len(variables))]
                # create mask based on lat, long extents
                mask = self.extents(latitude, longitude)
                # skip to next file if no matching stations are found
                if mask is None:
                    self.diagnostics(file)
                    continue
                # collect station IDs within the extent mask
                unique_id = np.unique(np.array(stationID[mask]))
                # write data to disk
                for i in range(len(unique_id)):
                    package = self.extract_station(stationID, str(unique_id[i]), *variables)
                    df = pd.DataFrame.from_dict(dict(zip(names, package)))
                    # time and temperature conversions
                    df[names[3]] = df[names[3]].apply(lambda x: datetime(1970, 1, 1) + timedelta(hours=(float(x)/3600)))
                    df[names[4]] = df[names[4]].apply(lambda x: (float(x) * 9/5) - 459.67)
                    df[names[8]] = df[names[8]].apply(lambda x: (float(x) * 9/5) - 459.67)
                    with open(CLEAN + str(unique_id[i]), 'a') as new_file:
                        df.to_csv(new_file, index=False, header=False)
                print('...time to clean file: {:.2f}'.format(time() - load_time))
        print('\n*time elapsed for cleaning entire batch: {:.2f}'.format(time() - start2))

    def get_files(self):

        """ CALLED by date_construct: get_files() """

        day_dl = time()
        print('starting download for next day')

        # loop through hours
        for k in range(24):
            dates = next(self.iter)
            http = ARCHIVE_URL + dates[0] + '/' + dates[1] + '/' + dates[2] + URL_MADIS + dates[0] + dates[1] + dates[2] + \
                dates[3] + '.gz'
            gz_file = http.split('/')[-1]
            file = gz_file.split('.')[0]
            hr_dl = time()
            print('downloading file: {}'.format(file))

            # attempt to connect to madis https server
            bck_off = 1
            with open(DL_DIR + gz_file, 'wb') as f:
                for attempt in range(1, 11):
                    try:
                        r = requests.get(http)
                        f.write(r.content)
                        str_error = None
                    except requests.exceptions.ConnectionError:
                        print('...error connecting to host')
                        str_error = True
                    if str_error:
                        sleep(bck_off)
                        bck_off *= 2
                        self.diagnostics(file, attempt, 0)
                    elif attempt == 10:
                        self.diagnostics(file, 1)
                        raise SystemExit('...unable to connect to host, terminating program at file: {}'.format(file))
                    else:
                        break

                print('...connection to host successful')

            try:
                with gzip.open(DL_DIR + gz_file, 'rb') as gz:
                    with open(DL_DIR + file, 'wb') as nc:
                        nc.write(gz.read())
            # catches missing files and continues to next iteration
            except OSError:
                print("...file {0} is not located on https server".format(file))
                self.diagnostics(file)
                os.remove(DL_DIR + gz_file)
                os.remove(DL_DIR + file)
                continue
            # catches corrupt (or possibly no contents to read in?) files and continues to next iteration
            except EOFError:
                print("...file {0} either corrupt or too small".format(file))
                self.diagnostics(file)
                os.remove(DL_DIR + gz_file)
                os.remove(DL_DIR + file)
                continue

            print('...time to download file: {:.2f}'.format(time() - hr_dl))
            os.remove(DL_DIR + gz_file)

        print('\n*time to download files for a single day: {:.2f}\n'.format(time() - day_dl))
        print('begin parsing and clean up operations')
        self.parse_files()
        for f in os.listdir(DL_DIR):
            os.remove(os.path.join(DL_DIR, f))
        print('*time elapsed for processing entire batch: {:.2f}'.format(time() - day_dl))
        print('*total time elapsed for entire process {:.2f}\n'.format(time() - self.start))
